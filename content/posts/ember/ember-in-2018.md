Title: Ember in 2018 and Beyond
Date: 2018-05-26
Category: Ember
Tags: ember, JavaScript
slug: ember-in-2018-and-beyond


This post reflects on my journey and impressions of the Ember.js framework so
far and some some ideas and wishes for Ember in 2018 and beyond.

The Ember.js framework has come a long way since i started to use it back in
2014. I remember when Ember used the "starter kit" and the transitions to the
Ember-CLI which inspired the CLI in Angular.

# The Journey with Ember so far

At the company i work at, we use both Angular and Ember.js for products and
internal tools. I have to say, having worked with several frameworks
over the past years, Ember.js is a joy to work with. Here are a few items that
stand out for me:

## Upgradability

The Ember.js framework takes compatibility very seriously. From my early days
with Ember.js, the framework releases followed semantic versioning. Every 6
weeks (roughly) a new minor version release comes out. This release cadence is
valuable in that it helps upgrades to be planned out. Every fourth release
becomes a LTS release (Long Time Support), which will be maintained with fixes
until the next LTS release is out. This way, some teams can plan to upgrade only
to LTS versions to limit the number of upgrades.

While Angular.js (version 1.x) projects had to go through major migration to
Angular 2 and beyond, our main Ember application was upgraded from 1.x to 2.x
and recently to version 3.1 in a fairly seamless fashion. As newer Ember.js
releases came out, deprecation messages guide the developer to use newer
constructs.

Knowing that the framework provides an upgrade path while still modernizing
itself, is a boon to large, long-running projects.

## Idioms and Conventions

When i initially heard about Ember's opinionated nature and strong conventions,
i feld it stifled development flexibility. In hindsight, having standard
conventions and project organization really makes things more manageable when
working with several developers and different Ember projects.

## Constructive Community

The community is one of Ember's great strenghts. There were times where i needed
help with the framework or an Ember addon, and each time I found solutions from
community members on the Ember.js slack channel, within minutes (for real!). The
Ember.js Learning Team does a great job with the user guides on the Ember.js
website, and the weekly newsletter and blog posts to share latest news about the
framework and its ecosystem. Also, the Ember Weekly news letter has been a
fantastic source of content and news about Ember for the past 3+ years.

The Ember community encourages its members to participate in the future
development of the framework, in the form of the RFC Process. Ember uses the RFC
(Request For Comments) process where major new framework features are proposed
and opened up to the community for feedback. This makes Ember very much a
community-driven framework, as opposed to be driven by a single sponsoring
company.

## Addon Ecosystem

The Ember Addon system has helped to package and share common Ember.js features
via npm modules. Whether you need UI components, authentication, app
deployment or server-side rendering, chances are: "There's an addon for that"
when you browse the catalog of addons on [Ember Observer](https://emberobserver.com/)
that seamlessly integrate with an Ember project, thanks to common convensions.


# On to 2018 and Beyond

Looking forward to Ember.js in 2018 and beyond, here are some items I think
would be good for the framework:

## Updated file layout structure

By default, when generating an Ember application using the Ember CLI, the source
files are structured in a way that groups the files by their types, as [seen here].
(https://ember-cli.com/user-guide/#module-directory-naming-structure)

Say you have a route called "Favorites" and the route uses a controller. That
means there will be three "favorite" files spread across three directories:

    :::Text
    ▾ controllers/
        favorites.js
    ▾ routes/
        favorites.js
    ▾ templates/
        favorites.hbs

My Ember.js projects use the alternative layout structure:
["PODS"](https://ember-cli.com/user-guide/#pod-structure). With PODS the files
are grouped by their entity, in this case there would be just one "favorites"
folder to group everything related to favorites together:

    :::Text
    ▾ favorites/
        controller.js
        route.js
        tempalte.hbs

This works nicely for the most part, but lacking in the following areas:

* there are still some general grouping directories, for example: helpers and
  initializers, which is not consistent with grouping files by entity.
* The entity grouping directories are all on the same level. That means, finding
  route-related files are not easy in large projects that have many grouping
  directories. What i did for my projects, was to name all the routes with a
  common "rte-" prefix, so that they would appear together in an alphabetized
  list of directories.
* All components are grouped under the "components" parent directory. It would
  be useful to be able to nest child components underneath a parent component's
  directory. Also, it would be useful to localize components within a route's
  directory.

There is a [Module Unification
RFC](https://github.com/emberjs/rfcs/blob/master/text/0143-module-unification.md)
that addresses these items and provides a very sensible file layout structure.
The RFC has been worked on for a while and is nearing completion. Ember core
team member Matthew Beale did an excellent [presentation on the Module
Unification](https://www.youtube.com/watch?v=M-ya4qmX4Nw) during EmberConf 2018.

While the Module Unification will be compatible with Ember addons that use the
historical file layout (and vice-versa), there will be a period with different
projects using differt file layouts. While Ember touts the strong conventions as
a productivity feature, having multiple conventions does not help much in that
regard.
Therefore, it would be great for the Ember framework to do a strong push to make
the Module Unification _the_ standard and encourage Ember Addon authors to
migrate to the new layout.


## Alternatives to the Ember Community Slack

As mentioned earlier, there have been many occasions where I found the Ember
Community Slack to be very valuable - finding the right answers to my questions
within minutes. There are very valuable nuggets of content in the various Ember
Slack channels, but unfortunately all that content is not discoverable if it
resides in Slack.


There is also the [Ember Disuss forum](https://discuss.emberjs.com/) which is
used but not as actively as the Ember Community Slack. I think the Ember
Discuss forum is great for posting longer content threads, whereas Slack excels
at quick and interactive exchanges with the community. 

How can we improve this so that valuable content is discoverable via web search?

Perhaps make an effort to use StackOverflow.com more for posting actual,
specific questions and use the Ember Community Slack for communication, and
linking to the StackOverflow posts. The
original intent of the Ember Forum was to discuss more involved topics that
might not have a specific answer.

Perhaps, if the Ember Discuss forum had a chat and notification feature it could
be an alternative to the Ember Slack team, and all content would be easily
discoverable. Some food for thought.


## Ease of adoption

Historically Ember has been a hard framework to learn. This has changed over
recent years, with various initiatives to simplify the framework and its API.

In my opinion, wide-spread adoption is still lagging because it's not easy
to adopt the Ember framework piecemeal. If it was easy to drop in Ember into an
existing app, it would really help boost the framework's adroption.

In the EmberConf 2017 keynote, the idea was presented to use the glimmer.js
rendering engine by itself, to implement a view layer with components. Then,
when more framework services (e.g. routing and data management) is needed, the
Ember modules can simply be incrementally `npm install`ed. This would be a good
approach to adopt Ember piecemeal when it materializes.

## Consumption of arbitrary npm modules

Currently Ember uses specially structured npm modules tagged as Ember Addons.
These work great and there is a rich collection of these on [Ember Observer](https://emberobserver.com/).
It would still be a good thing if any npm module could be easily consumed by
simply `npm install`ing it.

## Marketing of the Ember.js Framework

Ember.js is a fantastic framework that keeps innovating itself. A few examples
from the past years include being the first framework (as far as I can tell) to
introduce a CLI and server-side rendering (from way back in 2014), and the
Glimmer.js rendering engine that uses a VM to parse template "opcodes" and its
next step to use Binary Templates. More details in the [Glimmer.js Progress
Report](https://emberjs.com/blog/2017/10/10/glimmer-progress-report.html)

Yet, Ember suffers from a marketing problem among the other frameworks. This
might be due to several factors. While other new frameworks have emerged and
some have introduced newer versions with breaking changes (Angular 1.x to
Angular 2+ for example), it might leave the impression that Ember is still the
same Ember from 4 years ago.

There have been some positive communications efforts lately. The Ember Learning
Team does a good job with their weekly newsletter, and it's a great idea to
publish the newsletter on the official [Ember Blog](https://emberjs.com/blog/)
for added visibility and get it on search engines' web index.

Another thing the Ember Community can do whenever there's a Framework comparison
that omits the Ember framework, is to post a complementary blog post that
completes the framework comparison, with Ember included.

I would love to hear about ideas on this topic from other community members!

