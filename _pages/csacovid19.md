---
title: "ML Lab - COVID19"
layout: piclay
excerpt: "ML Lab -- COVID19"
permalink: /csacovid19/
---

COVID-19 PROJECTS FROM CSA, IISC
================================

## Project Title: Lockdown and other policies for containing COVID19 in Small worlds


##### Authors: V. Vinay (ATI Motors) and C. Bhattacharyya (CSA, IISc) 

##### Contact: chiru@iisc.ac.in, vinay@atimotors.com 


#### Our aim in this project is to understand what policies can be implemented post lockdown.

Small world models are useful tools in Network Epidemiology. A city consists of many wards. We model such cities as a Multi-Lattice Small World(MLSW) network where each ward of a city is modelled as a 2D lattice and nearby wards are connected together.  We simulate several interventions on MLSW and study their effectiveness in 

Suppressing COVID19 on such networks. Our study highlights three findings

1. Usual Contact Tracing involves Tracing the immediate contacts. If that can be enhanced to Tracing the contacts and their contacts followed by Sealing(TC2S) it would have a huge impact. 

2. A restricted work week, such as 2 day work week, followed by a Lockdown  can be effective as Lockdown.

3. A policy such as Ward wise sealing and Opening depending on the infection levels in the ward not only has the lowest attack rate, the percentage of total population infected, but also requires the shortest time for the epidemic to end.

#### A preliminary draft is available [here](https://drive.google.com/file/d/14UltuxOJE_CvM9qCvGXW_oj6puY6ame5/view) 


### Stay tuned for more projects 

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
