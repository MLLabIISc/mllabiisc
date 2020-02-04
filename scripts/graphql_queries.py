org_all_repos = """
query ($owner: String!, $endCursor: String) {
  organization(login: $owner) {
    repositories(first: 100, after: $endCursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
      edges {
        node {
          nameWithOwner
          name
          descriptionHTML
          homepageUrl
          isPrivate
          repositoryTopics(first: 50) {
            edges {
              node {
                topic {
                  name
                }
                url
              }
            }
          }
          primaryLanguage {
            name
            color
          }
          languages (first: 50) {
            edges {
              node {
                name
              }
              size
            }
          }
          pushedAt
          forkCount
          stargazers {
            totalCount
          }
          watchers {
            totalCount
          }
          defaultBranchRef{
              target{
                  ... on Commit {
                      history(first:10){
                          totalCount
                      }
                  }
              }
          }
          pull_request: pullRequests {
              totalCount
          }
          open_pull_request: pullRequests(states:[OPEN]) {
              totalCount
          }
          merged_pull_request: pullRequests(states:[MERGED]) {
              totalCount
          }
          closed_pull_request: pullRequests(states:[CLOSED]) {
              totalCount
          }
          issue: issues {
              totalCount
          }
          open_issue: issues(states:[OPEN]) {
              totalCount
          }
          closed_issue: issues(states:[CLOSED]) {
              totalCount
          }
        }
      }
    }
    membersWithRole {
      totalCount
    }
  }
}
"""

repo_wise = """
query ($owner:String!, $repo:String!) {
  repository(owner: $owner, name: $repo) {
    nameWithOwner
    name
    descriptionHTML
    homepageUrl
    isPrivate
    repositoryTopics(first: 50) {
      edges {
        node {
          topic {
            name
          }
          url
        }
      }
    }
    primaryLanguage {
      name
      color
    }
    languages (first: 50) {
      edges {
        node {
          name
        }
        size
      }
    }
    pushedAt
    forkCount
    stargazers {
      totalCount
    }
    watchers {
      totalCount
    }
    defaultBranchRef{
        target{
            ... on Commit {
                history(){
                    totalCount
                }
            }
        }        
    }
    pull_request: pullRequests {
        totalCount
    }
    open_pull_request: pullRequests(states:[OPEN]) {
        totalCount
    }
    merged_pull_request: pullRequests(states:[MERGED]) {
        totalCount
    }
    closed_pull_request: pullRequests(states:[CLOSED]) {
        totalCount
    }
    
    issue: issues {
        totalCount
    }
    open_issue: issues(states:[OPEN]) {
        totalCount
    }
    closed_issue: issues(states:[CLOSED]) {
        totalCount
    }
  }
}
"""
