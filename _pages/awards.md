---
title: "ML Lab - Awards"
layout: gridlay
excerpt: "ML Lab -- Awards."
sitemap: false
permalink: /awards
---


# Awards

## Highlights

(For a full list see [below](#full-list) or go to [Google Scholar](https://scholar.google.ch/citations?user=TqxYWZsAAAAJ), [ResearcherID](https://www.researcherid.com/rid/D-7763-2012))

{% assign number_printed = 0 %}
{% for award in site.data.awards %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if award.highlight == 1 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <pubtit>{{ award.title }}</pubtit>
<!--  <img src="{{ site.url }}{{ site.baseurl }}/images/pubpic/{{ award.image }}" class="img-responsive" width="33%" style="float: left" />-->
  <p>{{ award.description }}</p>
  <p><em>{{ award.authors }}</em></p>
  <p><strong><a href="{{ award.link.url }}">{{ award.link.display }}</a></strong></p>
  <p class="text-danger"><strong> {{ award.news1 }}</strong></p>
  <p> {{ award.news2 }}</p>
 </div>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endif %}
{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}

<p> &nbsp; </p>


## Full List

{% for award in site.data.awards %}

  {{ award.title }} <br />
  <em>{{ award.authors }} </em><br /><a href="{{ award.link.url }}">{{ award.link.display }}</a>

{% endfor %}

