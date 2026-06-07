May 26, 2026: GitHub recently detected a cyber-attack and immediately activated our response process to investigate, disrupt malicious activity, mitigate the attack, and deny the threat actor further access. It’s important to note that this investigation is still ongoing, and we will continue to provide details as appropriate.

Given the reality of threat actors and the advent of AI technologies, we need to do all we can to protect our customers. Considering the repositories that have been attacked and an abundance of caution, we are rotating keys, including the GitHub Enterprise Server signing key. This key is used to sign binaries for GitHub Enterprise Server to validate GitHub as the source during a manually initiated update process. All binaries hosted by GitHub are valid.

GitHub Enterprise Server customers need to take immediate action as described below. No action is required for GitHub Enterprise Cloud.

What customers need to do

GitHub Enterprise Server administrators will need to rotate the GPG public keys in their instance. Admins can follow these instructions to do so using a GitHub developed script to streamline the process. If you’d like to independently verify the integrity of the script, its SHA256 digest is:

Log on to any node in your HA or cluster installation and run the following commands, they will download the script, copy it to all nodes and run it on all nodes:

Note that the key is stored in both the admin and root accounts, so running a second time with sudo ensures that it is updated in both.

If the signing key is not rotated, future GitHub Enterprise Server version upgrades will fail verification with the following error message:

Error: The file provided is not a valid GitHub Enterprise Server package.

What this means for GitHub Enterprise Server customers

Future patches and releases will be signed with the new key, and customers will need to rotate to the new public key before those patches and releases can be installed. Customers should ensure they only download GHES updates from the official GitHub.com source URL. GitHub recommends that customers prepare to take GHES security updates at an increased rate over the coming months.

Looking ahead

As the information security landscape continues to evolve, we are prioritizing hardening our systems as new threats emerge. We’ll continue to update our community on noteworthy developments. We remain committed not only to keeping GitHub secure but also to helping secure the broader open source ecosystem.

Original blog post, published May 20, 2026: On Monday May 18, we detected and contained a compromise of an employee device involving a poisoned VS Code extension published by a third party. We removed the malicious extension version, isolated the endpoint, and began incident response immediately.

Our current assessment is that the activity involved exfiltration of GitHub-internal repositories only. The attacker’s current claims of ~3,800 repositories are directionally consistent with our investigation so far.

We have no evidence of impact to customer information stored outside of GitHub’s internal repositories, such as our customer’s own enterprises, organizations, and repositories. Some of GitHub’s internal repositories contain information from customers, for example, excerpts of support interactions. If any impact is discovered, we will notify customers via established incident response and notification channels.

We moved quickly to reduce risk. We rotated critical secrets Monday and into Tuesday with the highest-impact credentials prioritized first.

We continue to analyze logs, validate secret rotation, and monitor our infrastructure for any follow-on activity. We will take additional action as the investigation warrants.

We will publish a fuller report once the investigation is complete.

Alexis Wales is the Chief Information Security Officer of GitHub. She leads a team of security experts focused on safeguarding the GitHub platform, products and the open source community, empowering more than 150 million developers worldwide to build and deploy software securely on GitHub.

Alexis has 20 years of experience defending critical national and private sector networks, spanning positions with the Department of Defense and the Department of Homeland Security’s Cybersecurity and Infrastructure Security Agency (CISA). This experience sparked her passion for collaboration between the public and private sectors to solve the hardest security challenges that threaten the technology we use every day.

We’re updating our bug bounty program standards to prioritize quality submissions, clarify shared responsibility boundaries, and evolve how we reward low-risk findings.

Learn to find and exploit real-world agentic AI vulnerabilities through five progressive challenges in this free, open source game that over 10,000 developers have already used to sharpen their security skills.

We do newsletters, too

Discover tips, technical guides, and best practices in our biweekly newsletter just for devs.