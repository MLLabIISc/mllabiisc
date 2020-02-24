---
title: "ML Lab - Projects"
layout: textlay
excerpt: "Projects"
sitemap: false
permalink: /projects
---

# Projects

## Highlights

(For a list of publications, see [publications]("{{ site.url }}{{ site.baseurl }}/publications")

{% assign number_printed = 0 %}
{% for publi in site.data.projectlist %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if publi.highlight == 1 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <pubtit>{{ publi.title }}</pubtit>
  <img src="{{ site.url }}{{ site.baseurl }}/images/pubpic/{{ publi.image }}" class="img-responsive" width="33%" style="float:left; margin-right:10px;" />
  <p>{{ publi.description }}</p>
  <p><em>-{{ publi.authors }}</em></p>
  <p><strong><a href="{{ publi.link.url }}">{{ publi.link.display }}</a></strong></p>
  <!--<p class="text-danger"><strong> {{ publi.news1 }}</strong></p>--> <!--Rishabh - commented this because there is no project page as of now-->
  <p> {{ publi.news2 }}</p>
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
