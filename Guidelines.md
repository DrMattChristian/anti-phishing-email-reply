# List Format #

```
ADDRESS,TYPE,DATE
ADDRESS,TYPE,DATE
ADDRESS,TYPE,DATE
```

e.g.
```
accounthelpdesk@live.com,AC,20080327
windowsupgrades@microsoft.com,C,20080216
```

where:

**ADDRESS**: the full uid@domain email address that the phishing message is asking the user to reply to.  An _ADDRESS_ can only be listed once.  Only one _ADDRESS_ can be listed per line.

**TYPE**: the way the _ADDRESS_ was used.  Multiple types can be listed (e.g. 'ABCD' or 'AC' or 'B', etc)

  * A: The _ADDRESS_ was used in the Reply-To header.
  * B: The _ADDRESS_ was used in the From header.
  * C: The content of the phishing message contained the _ADDRESS_.
  * D: The content of the phishing message contained the _ADDRESS_ and it was obfuscated.
  * E: The ADDRESS (usually in the From header) might receive replies but it was not intended to receive the replies.

> Note: unless otherwise specified, in order for the ADDRESS to qualify for each TYPE, it must have been intended to receive the replies.

**DATE**: the date that the _ADDRESS_ was last seen used as the reply address in a phishing campaign.  Only one _DATE_ can be listed per line.