---
title: "ML Lab - Pictures"
layout: piclay
excerpt: "ML Lab -- Pictures"
permalink: /pictures/
---

# Pictures
Jump to: [Videos](#videos)


## Videos

#### Amazon AI Conclave 2018 - Academia view on AI by Prof.Chiranjib Bhattacharyya:
<iframe width="650" height="415" src="https://www.youtube.com/embed/8D7hXDVmzKU" frameborder="0" allowfullscreen></iframe>

#### NASSCOM Product Conclave 2016 - Speaking at DeepTech Summit by Prof.Chiranjib Bhattacharyya:
<iframe width="650" height="415" src="https://www.youtube.com/embed/gLtfhBa-Vo4" frameborder="0" allowfullscreen></iframe>

#### Gallery
(Right-click *'view image'* to see a larger image.)
{% assign number_printed = 0 %}
{% for pic in site.data.pictures_Leiden %}

{% assign even_odd = number_printed | modulo: 4 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
<img src="{{ site.url }}{{ site.baseurl }}/images/picpic/Gallery/{{ pic.image }}" class="img-responsive" width="95%" style="float: left" />
</div>

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

