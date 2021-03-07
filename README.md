# canvAssignments
## 2021 Spring HackHERS Winner for Best Use of In-Kind Sponsor Prize (Twilio)

## Table of Contents
- [Overview](#overview)
- [The Problem](#the-problem)
- [How canvAssignments solves this problem](#how-canvAssignments-solves-this-problem)
- [How it was built](#how-it-was-built)
- [What's next for canvAssignments](#whats-next-for-canvAssignments)
- [Other Resources](#other-resources)
- [License](#license)
- [Disclaimer](#disclaimer)


## Overview
canvAssignments makes it effortless for Rutgers Students to view their upcoming Canvas class assignments. Built using a Selenium Python Web Crawler hosted via a Python Flask backend onto a Twilio SMS service, canvAssignments creates a feature for students to view ALL of their upcoming assignments in two simple steps.  

## The Problem 
As student who are familiar with Canvas know, assignments for each class are spread out across the various course pages. Unfortunately, there lacks a feature where students can see all of their class assignments, simultaneously. This is where canvAssignments comes into play: it provides an easy way for students to view ALL of their upcoming assignments from ALL of their classes. 

## How canvAssignments solves this problem
canvAssignments allows students to send an SMS through Twilio's SMS service that is able to send back a list of all of the students' assignments. It simply asks for the students' NetID and password, logging them in through the Python Flask backend. The Selenium Web Crawler then makes its way through the page, utilizing BeautifulSoup to webscrape and return the users' assignments. 

## How it was built
canvAssignments was built using a Selenium Python Web Crawler integrated with Beautiful Soup. Once the crawler was able to extract the right imformation, it was implemented inside a Python Flask backend to process HTTP requests. This is how the application was able to POST the user's NetID and password to the website and create a new Web Crawler for each user. Once the POST method went through and the user was authenticated, the GET method was used to extract the list of assignments. Once the backend was finalized, it was implemented into Twilio's SMS messaging service so students were provided with an easy platform to request this information. 


