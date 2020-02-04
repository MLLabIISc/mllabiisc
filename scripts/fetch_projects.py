import os
import operator
import json
import requests

import re

import datetime

import graphql_queries
import string

PATH_TO_DATA = "_data"
GITHUB_USERNAME = os.environ["GH_USERNAME"]
GITHUB_OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
GITHUB_API_ENDPOINT = "https://api.github.com/graphql"

# This date is begin build project and count data
CONST_START_DATE = '2018-11-02'

print("LOG: Assuming the current path to be the root of the metrics repository.")

SVG_NO_OF_MEMBERS = 'N/A'
SVG_NO_OF_REPOS = 'N/A'

def get_previous_date(data_metrics, current_date):
    if len(data_metrics) == 0:
        return current_date

    list_dates = []
    for date_str in data_metrics:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        list_dates.append(date)
    previous_date = max(list_dates)

    return previous_date.strftime("%Y-%m-%d")

def fetch_one_page(query_string, variables):
    """
    Request the GitHub GraphQL API
    """
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(GITHUB_API_ENDPOINT, json={"query": query_string, "variables": variables}, auth=(GITHUB_USERNAME, GITHUB_OAUTH_TOKEN))
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Error in GitHub API query. Status Code : {}, Response: {}".format(r.status_code, r.json()))

# Number Contributors of Repository
def count_contributors_repository(repos):    
    r = requests.get("https://api.github.com/repos/" + repos + "/stats/contributors", auth=(GITHUB_USERNAME, GITHUB_OAUTH_TOKEN))
    numContributors = 0
    if r.status_code == 200:
        contributors = r.json()
        if isinstance(contributors[0], dict):
            numContributors = len(contributors)
    elif r.status_code == 202:
        rs = requests.get("https://api.github.com/repos/" + repos + "/stats/contributors", auth=(GITHUB_USERNAME, GITHUB_OAUTH_TOKEN), timeout=3)
        if rs.status_code == 200:
            contributors = rs.json()
            if isinstance(contributors[0], dict):
                numContributors = len(contributors)
    else:
        return 0
        #raise Exception("Error in GitHub API query. Status Code : {}, Response: {}".format(r.status_code, r.json()))

    return numContributors

all_org_edges = []  # All the repos in the org with their stats

# Read repos-to-include.txt
all_orgs = []  # Track orgs and all its repos e.g. DAI-Lab,..
all_repos = []  # Track specific repositories e.g. ('pantsbuild', 'pants')

with open("repos-to-include.txt", "r") as f:
    for line in f:
        owner, repo = line.split("/")
        repo = repo.rstrip("\n")
        if repo == "*":
            all_orgs.append(owner)
        else:
            all_repos.append((owner, repo))
print("LOG: Orgs to track", all_orgs)
print("Repos to track", all_repos)

for org in all_orgs:
    # Combine the paginated responses from the API
    has_next_page = False
    end_cursor = None
    num_of_pages = 0
    while True:
        print("Num of pages", num_of_pages)
        variables = json.dumps({"owner": org, "endCursor": end_cursor, "issues": {"states": "CLOSED"}})

        print("Sending request for", org)
        response = fetch_one_page(graphql_queries.org_all_repos, variables)
        print("Received request for", org)

        if response and response['data']:
            if response["data"]["organization"]["membersWithRole"]["totalCount"]:
                SVG_NO_OF_MEMBERS = response["data"]["organization"]["membersWithRole"]["totalCount"]

            repository_edges = response["data"]["organization"]["repositories"]["edges"]
            all_org_edges.extend(repository_edges)

            pageInfo = response["data"]["organization"]["repositories"]["pageInfo"]
            has_next_page = pageInfo["hasNextPage"]
            print("has_next_page", has_next_page)
            end_cursor = pageInfo["endCursor"]
            print("end_cursor", end_cursor)
            num_of_pages += 1
            if not has_next_page:
                break

print("LOG: Fetched all the org repositories. Count:", len(all_org_edges))
# print("LOG: First record")
# print(all_org_edges[0])

# Fetch individual repositories' data

all_repo_edges = []  # All individual repos

for repo in all_repos:
    variables = json.dumps({"owner": repo[0], "repo": repo[1], "endCursor": None})

    response = fetch_one_page(graphql_queries.repo_wise, variables)
    if response['errors']:
        continue
    if response and response['data']:
        all_repo_edges.append(response["data"])

print("LOG: Fetched all the individual repos as well. Count:", len(all_repo_edges))

# Repos to exclude
repos_to_exclude = set()
with open("repos-to-exclude.txt", "r") as f:
    for line in f:
        repo = line.rstrip("\n")
        repos_to_exclude.add(repo)

print("LOG: Removing private repositories")

public_repos = []
for edge in all_org_edges:
    if not edge["node"]["isPrivate"]:
        public_repos.append(edge)
for edge in all_repo_edges:
    if not edge["repository"]["isPrivate"]:
        public_repos.append({'node': edge['repository']})

DATA_JSON = {}
for repo in public_repos:
    #print(repo["node"])
    repo_full_name = repo["node"]["nameWithOwner"]
    if repo_full_name in repos_to_exclude:
        print("LOG: Excluding", repo_full_name)
        continue
    DATA_JSON[repo_full_name] = repo["node"]

    # Flatten list of languages
    languages_dict = {}
    for item in DATA_JSON[repo_full_name]["languages"]["edges"]:
        languages_dict[item["node"]["name"]] = item["size"]
    total_bytes = sum(languages_dict.values())
    for lang in languages_dict:
        languages_dict[lang] /= total_bytes  # This is got to be a float, so use Python 3

    # Use languages which have more than 5% code
    languages = []
    for item, value in languages_dict.items():
        if value > 0.05:
            languages.append(item)

    DATA_JSON[repo_full_name]["languages"] = " ".join(languages)

    # Flatten list of repository topics
    _topics = DATA_JSON[repo_full_name]["repositoryTopics"]["edges"]
    topics = []
    for item in _topics:
        topics.append(item["node"]["topic"]["name"])
    DATA_JSON[repo_full_name]["repositoryTopics"] = " ".join(topics)

    # Flatten stars count and watch count
    DATA_JSON[repo_full_name]["stargazers"] = DATA_JSON[repo_full_name]["stargazers"]["totalCount"]
    DATA_JSON[repo_full_name]["watchers"] = DATA_JSON[repo_full_name]["watchers"]["totalCount"]
    
    # Other information
    DATA_JSON[repo_full_name]["commits"] = 0
    if DATA_JSON[repo_full_name]["defaultBranchRef"]:
        DATA_JSON[repo_full_name]["commits"] = DATA_JSON[repo_full_name]["defaultBranchRef"]["target"]["history"]["totalCount"]
    DATA_JSON[repo_full_name]["pull_request"] = DATA_JSON[repo_full_name]["pull_request"]["totalCount"]
    DATA_JSON[repo_full_name]["open_pull_request"] = DATA_JSON[repo_full_name]["open_pull_request"]["totalCount"]
    DATA_JSON[repo_full_name]["merged_pull_request"] = DATA_JSON[repo_full_name]["merged_pull_request"]["totalCount"]
    DATA_JSON[repo_full_name]["closed_pull_request"] = DATA_JSON[repo_full_name]["closed_pull_request"]["totalCount"]
    DATA_JSON[repo_full_name]["issue"] = DATA_JSON[repo_full_name]["issue"]["totalCount"]
    DATA_JSON[repo_full_name]["open_issue"] = DATA_JSON[repo_full_name]["open_issue"]["totalCount"]
    DATA_JSON[repo_full_name]["closed_issue"] = DATA_JSON[repo_full_name]["closed_issue"]["totalCount"]
    # Contributors
    DATA_JSON[repo_full_name]["contributors"] = count_contributors_repository(repo_full_name)

    # descriptionHTML
    printable = set(string.printable)
    des = DATA_JSON[repo_full_name]["descriptionHTML"]
    des = ''.join(filter(lambda x: x in printable, des))
    description = re.sub(r'(<[^<+]+?>)|(\n)|(\t)', '', des)
    DATA_JSON[repo_full_name]["descriptionHTML"] = description

# Save to _data directory
file_path = PATH_TO_DATA + "/" + "projects.json"
with open(file_path, "w+") as f:
    json.dump(DATA_JSON, f)
print("LOG: Saved to", file_path)

SVG_NO_OF_REPOS = len(DATA_JSON)
print("LOG: Number of public repos", len(DATA_JSON))

# Statistics Summary
commits = 0
contributors = 0
for repo in DATA_JSON:
    commits = commits + DATA_JSON[repo]["commits"]
    contributors = contributors + DATA_JSON[repo]["contributors"]
DATA_STATISTICS = {
    "repositories": len(DATA_JSON),
    "commits": commits,
    "contributors": contributors
}
# Save to _data directory
file_path = PATH_TO_DATA + "/" + "statistics.json"
with open(file_path, "w+") as f:
    json.dump(DATA_STATISTICS, f)
print("LOG: Saved to", file_path)

# Set variable to store categories
CATEGORIES_JSON = []
for cate in all_orgs:
    subCate = []
    for repo in DATA_JSON:
        if repo.find(cate) != -1:
            subCate.append(DATA_JSON[repo]["name"])
    CATEGORIES_JSON.append({cate: subCate})

# Save categories to _data directory
file_path = PATH_TO_DATA + "/" + "categories.json"
with open(file_path, "w+") as f:
    json.dump(CATEGORIES_JSON, f)

DATA_METRIC = {}

# Calculate data for metrics
# WEEKDAY: 0-Monday, 6-Sunday.
# WEEKLY will run on Sunday. MONTHLY will run on 1st of month.
now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d")
# WEEKLY
if (now.weekday() == 6):
    for repo in DATA_JSON:
        #print(DATA_JSON[repo])
        # Create data file
        organization_repo_file = repo.replace('/', '__');
        DATA_METRIC = {}
        file_path = PATH_TO_DATA + "/" + organization_repo_file + "_weekly.json"
        if os.path.exists(file_path):
            with open(file_path) as f:
                DATA_METRIC = json.load(f)
        # New data from server
        previous_date_weekly = get_previous_date(DATA_METRIC, now_str)
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": previous_date_weekly,
            "commitCount": DATA_JSON[repo]["commits"],
            "issueCount": DATA_JSON[repo]["issue"],
            "openIssueCount": DATA_JSON[repo]["open_issue"],
            "closedIssueCount": DATA_JSON[repo]["closed_issue"],
            "pullRequestCount": DATA_JSON[repo]["pull_request"],
            "openPullRequestCount": DATA_JSON[repo]["open_pull_request"],
            "mergedPullRequestCount": DATA_JSON[repo]["merged_pull_request"],
            "closedPullRequestCount": DATA_JSON[repo]["closed_pull_request"],
            "forkCount": DATA_JSON[repo]["forkCount"],
            "starCount": DATA_JSON[repo]["stargazers"],
            "watcherCount": DATA_JSON[repo]["watchers"],
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of repository
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)

    # Calculate for Organization
    numRow = 0
    for repo in DATA_JSON:
        numRow = numRow + 1
        # New data from server
        organization = repo.split("/")
        organizationName = organization[0]
        if numRow > 1 and repo.find(organizationName):
            continue
        # Initial data for organization
        commitCount = 0
        issueCount = 0
        openIssueCount = 0
        closedIssueCount = 0
        pullRequestCount = 0
        openPullRequestCount = 0
        mergedPullRequestCount = 0
        closedPullRequestCount = 0
        forkCount = 0
        starCount = 0
        watcherCount = 0
        for repo2 in DATA_JSON:
            if repo2.find(organizationName) != -1:
                commitCount = commitCount + DATA_JSON[repo2]["commits"]
                issueCount = issueCount + DATA_JSON[repo2]["issue"]
                openIssueCount = openIssueCount + DATA_JSON[repo2]["open_issue"]
                closedIssueCount = closedIssueCount + DATA_JSON[repo2]["closed_issue"]
                pullRequestCount = pullRequestCount + DATA_JSON[repo2]["pull_request"]
                openPullRequestCount = openPullRequestCount + DATA_JSON[repo2]["open_pull_request"]
                mergedPullRequestCount = mergedPullRequestCount + DATA_JSON[repo2]["merged_pull_request"]
                closedPullRequestCount = closedPullRequestCount + DATA_JSON[repo2]["closed_pull_request"]
                forkCount = forkCount + DATA_JSON[repo2]["forkCount"]
                starCount = starCount + DATA_JSON[repo2]["stargazers"]
                watcherCount = watcherCount + DATA_JSON[repo2]["watchers"]
        
        #print(DATA_JSON[repo])
        # Create data file
        organization_repo_file = organizationName;
        DATA_METRIC = {}
        file_path = PATH_TO_DATA + "/" + organization_repo_file + "_weekly.json"
        if os.path.exists(file_path):
            with open(file_path) as f:
                DATA_METRIC = json.load(f)

        previous_date_weekly = get_previous_date(DATA_METRIC, now_str)
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": previous_date_weekly,
            "commitCount": commitCount,
            "issueCount": issueCount,
            "openIssueCount": openIssueCount,
            "closedIssueCount": closedIssueCount,
            "pullRequestCount": pullRequestCount,
            "openPullRequestCount": openPullRequestCount,
            "mergedPullRequestCount": mergedPullRequestCount,
            "closedPullRequestCount": closedPullRequestCount,
            "forkCount": forkCount,
            "starCount": starCount,
            "watcherCount": watcherCount,
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of organization
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)


# MONTHLY
if (now.strftime("%d") == '01' or now.strftime("%d") == '1'):
    for repo in DATA_JSON:
        # Create data file
        organization_repo_file = repo.replace('/', '__');
        DATA_METRIC = {}
        file_path = PATH_TO_DATA + "/" + organization_repo_file + "_monthly.json"
        if os.path.exists(file_path):
            with open(file_path) as f:
                DATA_METRIC = json.load(f)

        previous_date_monthly = get_previous_date(DATA_METRIC, now_str)
        # New data from server
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": previous_date_monthly,
            "commitCount": DATA_JSON[repo]["commits"],
            "issueCount": DATA_JSON[repo]["issue"],
            "openIssueCount": DATA_JSON[repo]["open_issue"],
            "closedIssueCount": DATA_JSON[repo]["closed_issue"],
            "pullRequestCount": DATA_JSON[repo]["pull_request"],
            "openPullRequestCount": DATA_JSON[repo]["open_pull_request"],
            "mergedPullRequestCount": DATA_JSON[repo]["merged_pull_request"],
            "closedPullRequestCount": DATA_JSON[repo]["closed_pull_request"],
            "forkCount": DATA_JSON[repo]["forkCount"],
            "starCount": DATA_JSON[repo]["stargazers"],
            "watcherCount": DATA_JSON[repo]["watchers"],
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of repository
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)
            
    # Calculate for Organization
    numRow = 0
    for repo in DATA_JSON:
        numRow = numRow + 1
        # New data from server
        organization = repo.split("/")
        organizationName = organization[0]
        if numRow > 1 and repo.find(organizationName):
            continue
        # Initial data for organization
        commitCount = 0
        issueCount = 0
        openIssueCount = 0
        closedIssueCount = 0
        pullRequestCount = 0
        openPullRequestCount = 0
        mergedPullRequestCount = 0
        closedPullRequestCount = 0
        forkCount = 0
        starCount = 0
        watcherCount = 0
        for repo2 in DATA_JSON:
            if repo2.find(organizationName) != -1:
                commitCount = commitCount + DATA_JSON[repo2]["commits"]
                issueCount = issueCount + DATA_JSON[repo2]["issue"]
                openIssueCount = openIssueCount + DATA_JSON[repo2]["open_issue"]
                closedIssueCount = closedIssueCount + DATA_JSON[repo2]["closed_issue"]
                pullRequestCount = pullRequestCount + DATA_JSON[repo2]["pull_request"]
                openPullRequestCount = openPullRequestCount + DATA_JSON[repo2]["open_pull_request"]
                mergedPullRequestCount = mergedPullRequestCount + DATA_JSON[repo2]["merged_pull_request"]
                closedPullRequestCount = closedPullRequestCount + DATA_JSON[repo2]["closed_pull_request"]
                forkCount = forkCount + DATA_JSON[repo2]["forkCount"]
                starCount = starCount + DATA_JSON[repo2]["stargazers"]
                watcherCount = watcherCount + DATA_JSON[repo2]["watchers"]
        
        #print(DATA_JSON[repo])
        # Create data file
        organization_repo_file = organizationName;
        DATA_METRIC = {}
        file_path = PATH_TO_DATA + "/" + organization_repo_file + "_monthly.json"
        if os.path.exists(file_path):
            with open(file_path) as f:
                DATA_METRIC = json.load(f)

        previous_date_monthly = get_previous_date(DATA_METRIC, now_str)
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": previous_date_monthly,
            "commitCount": commitCount,
            "issueCount": issueCount,
            "openIssueCount": openIssueCount,
            "closedIssueCount": closedIssueCount,
            "pullRequestCount": pullRequestCount,
            "openPullRequestCount": openPullRequestCount,
            "mergedPullRequestCount": mergedPullRequestCount,
            "closedPullRequestCount": closedPullRequestCount,
            "forkCount": forkCount,
            "starCount": starCount,
            "watcherCount": watcherCount,
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of organization
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)

# Update the SVG
print("No of members", SVG_NO_OF_MEMBERS)
print("No of repos", SVG_NO_OF_REPOS)
network_svg = open("assets/network_raw.svg").read()
network_svg = network_svg.replace("{$members}", str(SVG_NO_OF_MEMBERS))
network_svg = network_svg.replace("{$Repos}", str(SVG_NO_OF_REPOS))
with open("assets/network.svg", "w+") as f:
    f.write(network_svg)
print("LOG: assets/network.svg updated!")

# GENERATE TEMPLATE FILE
PATH_TO_METRICS = "metrics"
URL_METRICS = "/metrics"

def write_template_file(file_path, layout, permalink, title, options={}):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w+") as f:
        f.write("---\n")
        f.write("layout: '{0}'\n".format(layout))
        f.write("permalink: '{0}'\n".format(permalink))
        f.write("title: '{0}'\n".format(title))
        for keyField in options:
            f.write(str(keyField) + ": '" + options[keyField] + "'\n")
        f.write("---\n")

# Create template for repository weekly
def create_template_repository_weekly(cate, subCate, now_str):
    organization_folder_path = PATH_TO_METRICS + "/" + cate + "/" + subCate
    # Index page
    organization_path = organization_folder_path + "/index.md"
    layout = "repository"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/"
    title = "DAI Lab OSS Metrics Metrics report for " + subCate
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    # WEEKLY page
    organization_path = organization_folder_path + "/WEEKLY.md"
    layout = "weekly"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/WEEKLY" + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ subCate +" | WEEKLY-REPORT-" + now_str
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # WEEKLY DATE page
    organization_path = organization_folder_path + "/WEEKLY-REPORT-"+ now_str +".md"
    layout = "weekly"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/WEEKLY-REPORT-"+ now_str
    title = "DAI Lab OSS Metrics Metrics report for "+ subCate +" | WEEKLY-REPORT-" + now_str
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)

# Create template for organization weekly
def create_template_organization_weekly(cate, now_str):
    organization_folder_path = PATH_TO_METRICS + "/" + cate
    # Index page
    organization_path = organization_folder_path + "/index.md"
    layout = "organization"
    permalink = URL_METRICS + "/" + cate + "/"
    title = "Index"
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    # WEEKLY page
    organization_path = organization_folder_path + "/WEEKLY.md"
    layout = "organization_weekly"
    permalink = URL_METRICS + "/" + cate + "/WEEKLY" + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ cate +" | WEEKLY-REPORT-" + now_str
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # WEEKLY DATE page
    organization_path = organization_folder_path + "/WEEKLY-REPORT-"+ now_str +".md"
    layout = "organization_weekly"
    permalink = URL_METRICS + "/" + cate + "/WEEKLY-REPORT-"+ now_str + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ cate +" | WEEKLY-REPORT-" + now_str
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    

# Generate template
# WEEKLY
if (now.weekday() == 6):
    for listCate in CATEGORIES_JSON:
        for cate in listCate:
            create_template_organization_weekly(cate, now_str)
            #Generate template for sub-categories
            for subCate in listCate[cate]:
                create_template_repository_weekly(cate, subCate, now_str)

# Create template repository monthly
def create_template_repository_monthly(cate, subCate, now_str):
    organization_folder_path = PATH_TO_METRICS + "/" + cate + "/" + subCate
    # Index page
    organization_path = organization_folder_path + "/index.md"
    layout = "repository"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/"
    title = "DAI Lab OSS Metrics Metrics report for " + subCate
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # MONTHLY page
    organization_path = organization_folder_path + "/MONTHLY.md"
    layout = "monthly"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/MONTHLY" + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ subCate +" | MONTHLY-REPORT-" + now_str
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # MONTHLY DATE page
    organization_path = organization_folder_path + "/MONTHLY-REPORT-"+ now_str +".md"
    layout = "monthly"
    permalink = URL_METRICS + "/" + cate + "/" + subCate + "/MONTHLY-REPORT-"+ now_str + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ subCate +" | MONTHLY-REPORT-" + now_str
    options = {"organization": cate, "repository": subCate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)

# Create template organization monthly
def create_template_organization_monthly(cate, now_str):
    organization_folder_path = PATH_TO_METRICS + "/" + cate
    # Index page
    organization_path = organization_folder_path + "/index.md"
    layout = "organization"
    permalink = URL_METRICS + "/" + cate + "/"
    title = "Index"
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # MONTHLY page
    organization_path = organization_folder_path + "/MONTHLY.md"
    layout = "organization_monthly"
    permalink = URL_METRICS + "/" + cate + "/MONTHLY" + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ cate +" | MONTHLY-REPORT-" + now_str
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)
    
    # MONTHLY DATE page
    organization_path = organization_folder_path + "/MONTHLY-REPORT-"+ now_str +".md"
    layout = "organization_monthly"
    permalink = URL_METRICS + "/" + cate + "/MONTHLY-REPORT-"+ now_str + "/"
    title = "DAI Lab OSS Metrics Metrics report for "+ cate +" | MONTHLY-REPORT-" + now_str
    options = {"organization": cate, "current_date": now_str}
    write_template_file(organization_path, layout, permalink, title, options)

# MONTHLY
if (now.strftime("%d") == '01' or now.strftime("%d") == '1'):
    for listCate in CATEGORIES_JSON:
        for cate in listCate:
            create_template_organization_monthly(cate, now_str)
            #Generate template for sub-categories
            for subCate in listCate[cate]:
                create_template_repository_monthly(cate, subCate, now_str)

# CALCULATE DATA WEEKLY - MONTHLY FOR NEW REPOSITORY (THEY ARE NOT EXIST BECAUSE THIS DAY IS NOT WEEKLY DAY OR MONTHLY DAY)
# CASE: WEEKLY
# WEEKLY: Repository
for repo in DATA_JSON:
    # Create data file
    organization = repo.split("/")
    organizationName = organization[0]
    repositoryName = organization[1]

    organization_repo_file = repo.replace('/', '__');
    DATA_METRIC = {}
    file_path = PATH_TO_DATA + "/" + organization_repo_file + "_weekly.json"
    if not os.path.exists(file_path):
        # New data from server
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": now_str,
            "commitCount": DATA_JSON[repo]["commits"],
            "issueCount": DATA_JSON[repo]["issue"],
            "openIssueCount": DATA_JSON[repo]["open_issue"],
            "closedIssueCount": DATA_JSON[repo]["closed_issue"],
            "pullRequestCount": DATA_JSON[repo]["pull_request"],
            "openPullRequestCount": DATA_JSON[repo]["open_pull_request"],
            "mergedPullRequestCount": DATA_JSON[repo]["merged_pull_request"],
            "closedPullRequestCount": DATA_JSON[repo]["closed_pull_request"],
            "forkCount": DATA_JSON[repo]["forkCount"],
            "starCount": DATA_JSON[repo]["stargazers"],
            "watcherCount": DATA_JSON[repo]["watchers"],
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of repository
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)
        # Create template repository weekly
        create_template_repository_weekly(organizationName, repositoryName, now_str)

# WEEKLY: Organization
# Calculate for Organization
numRow = 0
for repo in DATA_JSON:
    numRow = numRow + 1
    # New data from server
    organization = repo.split("/")
    organizationName = organization[0]
    if numRow > 1 and repo.find(organizationName):
        continue
    organization_repo_file = organizationName
    file_path = PATH_TO_DATA + "/" + organization_repo_file + "_weekly.json"
    if not os.path.exists(file_path):
        # Initial data for organization
        commitCount = 0
        issueCount = 0
        openIssueCount = 0
        closedIssueCount = 0
        pullRequestCount = 0
        openPullRequestCount = 0
        mergedPullRequestCount = 0
        closedPullRequestCount = 0
        forkCount = 0
        starCount = 0
        watcherCount = 0
        for repo2 in DATA_JSON:
            if repo2.find(organizationName) != -1:
                commitCount = commitCount + DATA_JSON[repo2]["commits"]
                issueCount = issueCount + DATA_JSON[repo2]["issue"]
                openIssueCount = openIssueCount + DATA_JSON[repo2]["open_issue"]
                closedIssueCount = closedIssueCount + DATA_JSON[repo2]["closed_issue"]
                pullRequestCount = pullRequestCount + DATA_JSON[repo2]["pull_request"]
                openPullRequestCount = openPullRequestCount + DATA_JSON[repo2]["open_pull_request"]
                mergedPullRequestCount = mergedPullRequestCount + DATA_JSON[repo2]["merged_pull_request"]
                closedPullRequestCount = closedPullRequestCount + DATA_JSON[repo2]["closed_pull_request"]
                forkCount = forkCount + DATA_JSON[repo2]["forkCount"]
                starCount = starCount + DATA_JSON[repo2]["stargazers"]
                watcherCount = watcherCount + DATA_JSON[repo2]["watchers"]

        # Create data file
        DATA_METRIC = {}
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": now_str,
            "commitCount": commitCount,
            "issueCount": issueCount,
            "openIssueCount": openIssueCount,
            "closedIssueCount": closedIssueCount,
            "pullRequestCount": pullRequestCount,
            "openPullRequestCount": openPullRequestCount,
            "mergedPullRequestCount": mergedPullRequestCount,
            "closedPullRequestCount": closedPullRequestCount,
            "forkCount": forkCount,
            "starCount": starCount,
            "watcherCount": watcherCount,
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of organization
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)
        # Create template organization weekly
        create_template_organization_weekly(organizationName, now_str)

# CASE: MONTHLY
# MOTHLY: Repository
for repo in DATA_JSON:
    # Create data file
    organization = repo.split("/")
    organizationName = organization[0]
    repositoryName = organization[1]

    organization_repo_file = repo.replace('/', '__');
    DATA_METRIC = {}
    file_path = PATH_TO_DATA + "/" + organization_repo_file + "_monthly.json"
    if not os.path.exists(file_path):
        # New data from server
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": now_str,
            "commitCount": DATA_JSON[repo]["commits"],
            "issueCount": DATA_JSON[repo]["issue"],
            "openIssueCount": DATA_JSON[repo]["open_issue"],
            "closedIssueCount": DATA_JSON[repo]["closed_issue"],
            "pullRequestCount": DATA_JSON[repo]["pull_request"],
            "openPullRequestCount": DATA_JSON[repo]["open_pull_request"],
            "mergedPullRequestCount": DATA_JSON[repo]["merged_pull_request"],
            "closedPullRequestCount": DATA_JSON[repo]["closed_pull_request"],
            "forkCount": DATA_JSON[repo]["forkCount"],
            "starCount": DATA_JSON[repo]["stargazers"],
            "watcherCount": DATA_JSON[repo]["watchers"],
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of repository
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)
        # Create repository monthly
        create_template_repository_monthly(organizationName, repositoryName, now_str)
        
# MONTHLY: Organization
# Calculate for Organization
numRow = 0
for repo in DATA_JSON:
    numRow = numRow + 1
    # New data from server
    organization = repo.split("/")
    organizationName = organization[0]
    
    if numRow > 1 and repo.find(organizationName):
        continue

    organization_repo_file = organizationName;
    file_path = PATH_TO_DATA + "/" + organization_repo_file + "_monthly.json"    
    if not os.path.exists(file_path):    
        # Initial data for organization
        commitCount = 0
        issueCount = 0
        openIssueCount = 0
        closedIssueCount = 0
        pullRequestCount = 0
        openPullRequestCount = 0
        mergedPullRequestCount = 0
        closedPullRequestCount = 0
        forkCount = 0
        starCount = 0
        watcherCount = 0
        for repo2 in DATA_JSON:
            if repo2.find(organizationName) != -1:
                commitCount = commitCount + DATA_JSON[repo2]["commits"]
                issueCount = issueCount + DATA_JSON[repo2]["issue"]
                openIssueCount = openIssueCount + DATA_JSON[repo2]["open_issue"]
                closedIssueCount = closedIssueCount + DATA_JSON[repo2]["closed_issue"]
                pullRequestCount = pullRequestCount + DATA_JSON[repo2]["pull_request"]
                openPullRequestCount = openPullRequestCount + DATA_JSON[repo2]["open_pull_request"]
                mergedPullRequestCount = mergedPullRequestCount + DATA_JSON[repo2]["merged_pull_request"]
                closedPullRequestCount = closedPullRequestCount + DATA_JSON[repo2]["closed_pull_request"]
                forkCount = forkCount + DATA_JSON[repo2]["forkCount"]
                starCount = starCount + DATA_JSON[repo2]["stargazers"]
                watcherCount = watcherCount + DATA_JSON[repo2]["watchers"]
        
        # Create data file
        DATA_METRIC = {}
        repoMetrics = {
            "current_date": now_str, 
            "previous_date": now_str,
            "commitCount": commitCount,
            "issueCount": issueCount,
            "openIssueCount": openIssueCount,
            "closedIssueCount": closedIssueCount,
            "pullRequestCount": pullRequestCount,
            "openPullRequestCount": openPullRequestCount,
            "mergedPullRequestCount": mergedPullRequestCount,
            "closedPullRequestCount": closedPullRequestCount,
            "forkCount": forkCount,
            "starCount": starCount,
            "watcherCount": watcherCount,
        }
        DATA_METRIC[now_str] = repoMetrics
        #save metrics data of organization
        with open(file_path, "w+") as f:
            json.dump(DATA_METRIC, f)
        # Create template organization monthly
        create_template_organization_monthly(organizationName, now_str)