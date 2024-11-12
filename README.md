![Senior os logo](https://fee9.short.gy/SOS-logo-git.png)

# Senior-OS

**This work is in progress and for testing purposes only**

Working environment for late seniors and cognitive challenged users (e.g. Alzheimer's disease, Down syndrome)

## Description

Late seniors and cognitive challenged users encounter difficulties when using common desktop systems and require assistance from their caregivers. They are also easy targets for cyber criminals. This project aims to provide a working environment suitable for such users and improve their online security.

## Key features

- Very simple layout for easy use
- All actions linked to familiar person photos or large icons
- Levels of security protection based on user mental ability
- Caregiver notifications to solve problems quickly
- Available as live ISO with persistent configuration

## Instructions

Instuctions for development testing

TODO
 
## Environment applications

- [Email client](https://github.com/forsenior/senior-os/tree/main/smail) for senior
- [Web browser](https://github.com/forsenior/senior-os/tree/main/sweb) for senior
- [Configuraton](https://github.com/forsenior/senior-os/tree/main/sconf) for senior caregiver
- [App runner](https://github.com/forsenior/senior-os/tree/main/srun) for senior
- [Live OS builder](https://github.com/forsenior/senior-os/tree/main/siso) for developers

## Protection levels

Three protection levels (PL) are provided based on user mental ability

PL3 Strong - for users with severe mental impairment, e.g. Alzheimer's disease

1. Browsing limited to whitelisted webpages
2. Receiving and sending emails only to/from whitelisted persons

PL2 Moderate - for users with light to medium mental impairment, e.g. Down syndrome

1. Disabled text input on all webpages, web search allowed
2. Receiving emails only from whitelisted persons
3. Red-alert* on sending email with sensitive information (card number, password, address)

PL1 Light - for users with online good-practice problems, e.g. seniors over 90

1. Red-alert* on visiting phishing webpages
3. Red-alert* on sending email with sensitive information
3. Caregiver email with copy of phishing filled-in form
4. Caregiver email with copy of sent sensitive information

*Red-alert is strong visual warning

## Visual example

![Visual example](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_sensitive_information_alert.png)

## Student contribution

Students can contribute to the development by their bachelor's and master's theses 

List of current topics is [here](https://github.com/forsenior/senior-os/tree/main/theses) (in Czech)
