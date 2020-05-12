---
title: "ML Lab - COVID19"
layout: piclay
excerpt: "ML Lab -- COVID19"
permalink: /csacovid19/
---

<h1 style="color:red; text-align:center;">COVID-19 PROJECTS FROM CSA, IISC</h1>
<hr style="width:100%;text-align:center;margin-left:0;height:10px;color:#1B374C">
<h2 style="color:#108896"> Project Title: Lockdown and other policies for containing COVID19 in Small worlds </h2>
<hr style="width:100%;text-align:center;margin-left:0;height:10px;color:#1B374C">

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

<hr style="width:100%;text-align:center;margin-left:0;height:10px;color:#1B374C">
<h2 style="color:#108896"> Project Title: CovidWATCH </h2>
<hr style="width:100%;text-align:center;margin-left:0;height:10px;color:#1B374C">

### Lead Developers: Niharika Venkatesh(AIfoundry) and Nabanita Paul(IISc) 

### Advised by Arvind Saraf(AIfoundry) and Chiranjib Bhattacharyya(IISc)

##### COLLABORATION BETWEEN INDIAN INSTITUTE OF SCIENCE (IISC) & AI FOUNDRY, BENGALURU

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
