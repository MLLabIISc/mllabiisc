---
title: "ML Lab - COVID19"
layout: piclay
excerpt: "ML Lab -- COVID19"
permalink: /csacovid19/
---

<h1 style="color:red; text-align:center; font-size: 50px; font-family: -webkit-pictograph; inline-size: -webkit-fill-available; line-height:2; box-shadow: 0px 0px 10px 0px #106a8c; text-shadow: -2px 3px 3px #333;">COVID-19 PROJECTS FROM CSA, IISC</h1>
<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">
<h2 style="color:#108896"> Project 1: Lockdown and other policies for containing COVID19 in Small worlds </h2>
<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">

##### Authors: V. Vinay (ATI Motors) and C. Bhattacharyya (CSA, IISc) 

##### Contact: vinay@atimotors.com, chiru@iisc.ac.in

<br>

<h5><u> Our aim in this project is to understand what policies can be implemented post lockdown.</u></h5>

Small world models are useful tools in Network Epidemiology. A city consists of many wards. We model such cities as a Multi-Lattice Small World(MLSW) network where each ward of a city is modelled as a 2D lattice and nearby wards are connected together.  We simulate several interventions on MLSW and study their effectiveness in 

Suppressing COVID19 on such networks. Our study highlights three findings

1. Usual Contact Tracing involves Tracing the immediate contacts. If that can be enhanced to Tracing the contacts and their contacts followed by Sealing(TC2S) it would have a huge impact. 

2. A restricted work week, such as 2 day work week, followed by a Lockdown  can be effective as Lockdown.

3. A policy such as Ward wise sealing and Opening depending on the infection levels in the ward not only has the lowest attack rate, the percentage of total population infected, but also requires the shortest time for the epidemic to end.

##### A preliminary draft is available [here](https://drive.google.com/file/d/14UltuxOJE_CvM9qCvGXW_oj6puY6ame5/view) 

#### Press Coverage: [Sealing areas with higher Covid-19 cases or 2-day work week with lockdown can contain virus, shorten epidemic duration: Analysis - mumbai news - Hindustan Times](https://www.hindustantimes.com/mumbai-news/sealing-areas-with-higher-covid-19-cases-or-2-day-work-week-with-lockdown-can-contain-virus-shorten-epidemic-duration-analysis/story-4XQBmv4KaJ4yBoZmgEI51I.html)

<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">
<h2 style="color:#108896"> Project 2: CovidWATCH - A rapid COVID-19 monitoring tool for regions with low smartphone penetration </h2>
<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">

##### Lead Developers: Niharika Venkatesh(AIfoundry) and Nabanita Paul(IISc) 

##### Contact: niharika@aifoundry.ai, nabanitapaul@iisc.ac.in

##### Advised by: Arvind Saraf(AIfoundry) and Chiranjib Bhattacharyya(IISc)

##### Contact: arvind@aifoundry.ai, chiru@iisc.ac.in

<br>

<h4><i>COLLABORATION BETWEEN INDIAN INSTITUTE OF SCIENCE (IISC) & AI FOUNDRY, BENGALURU</i></h4>

<br>

<h5><u> Covid Watch is a rapid monitoring tool developed for areas with low smartphone penetration.</u></h5>

It offers a basic screening test based on ICMR strategy and a symptom tracker to record daily symptoms, via multi-language Whatsapp chatbot. Specifically built for people with little to no technological acumen, it also allows a single volunteer to take this test on behalf of multiple nearby people for convenience. The data is shared with the authorities in form of a dashboard, where they filter based on location, symptoms,age,etc. for subsequent follow ups. This tool has been deployed in a ward under Pune Municipality and has already helped authorities by surveying close to 3000 people in ~2 weeks. 

A slide deck detailing the tool is available [here](https://drive.google.com/open?id=1G6fbV0fzH9Xo9_y2zdZqnmEQRgpoJ8bc).

<br>

<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">
<h2 style="color:#108896"> Project 3: COVID SWIFT - RAPID AI SOLUTIONS </h2>
<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">

##### Lead Developers: Sabyasachi Saho(IISc), Prashant Kumar(IISc), Santosh Shet(IISc), Siva Teja Kakileti(Niramai), and Hariharan Vijayakumar(Niramai)

##### Contact: sabyasachis@iisc.ac.in, prashantkumar12@iisc.ac.in, santo.shet@gmail.com, sivateja@niramai.com, hariharan@niramai.com

##### Advised by: Chiranjib Bhattacharyya(IISc), Geetha Manjunath(Niramai), and Dr. Padmanabha Kamath(KMC)

##### Contact: chiru@iisc.ac.in, swift@niramai.com

<br>

<h4><i>COLLABORATION BETWEEN INDIAN INSTITUTE OF SCIENCE (IISC), NIRAMAI & KMC, BENGALURU</i></h4>

<br>

<h5><u> COVID SWIFT is a Rapid AI solution for Diagnosing COVID-19 using Chest X-RAY</u></h5>

We use state of art deep learning models to provide with likely COVID-19 and Pneumonia predictions. Our aim is to identify affected lung regions that can help doctors understand the severity of illness of their patients.


This is a free Whatsapp based service to provide with swift diagnosis of potential COVID19 patients by analyzing Chest X-Ray images. We are running a small scale pilot where interested doctors within minutes, can receive a machine generated X-ray Report (as the one shown below) on sending us chest X-Ray of suspicious patients.

For more information on this please visit [COVID SWIFT](http://bit.ly/covid-swift).

<br>

<hr style="width:100%;text-align:center;margin-left:0;height:10px; border-color: #ec511f; border-width: thick;">


<h4 style="text-align:center; color:red;">Stay tuned for more projects!</h4> 

{% assign number_printed = 0 %}
{% for pic in site.data.pictures_Leiden %}

{% assign even_odd = number_printed | modulo: 4 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd > 2 %}
</div>
{% endif %}


{% endfor %}

{% assign even_odd = number_printed | modulo: 4 %}
{% if even_odd == 1 %}
</div>
{% endif %}

{% if even_odd == 2 %}
</div>
{% endif %}

{% if even_odd == 3 %}
</div>
{% endif %}

<p> &nbsp; </p>
