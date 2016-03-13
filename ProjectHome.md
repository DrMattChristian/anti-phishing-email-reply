## Description ##

### What this project **is** ###

This project is intended to organize email service provider response to email phishing campaigns that convince the end-user to reply via email with their information.

The intent of this project is to maintain a list of accounts that are being used (or have been used) in the reply-to address of phishing campaigns.  Email service administrators can use this list to actively block outgoing smtp submissions destined for these accounts.  The list can also be used to scan recent SMTP logs to determine if any users have already replied.

This project may also be used to host tools to aid in reformatting the list for automatic import into various email server configurations.

### What this project **is not** ###

There are many projects aimed at stopping or identifying inbound email phishing messages.  This project is not intended to be one of them.

Since the scammers frequently hijack legitimate accounts, there is a high likelihood that legitimate email addresses make it onto this list.

The maintainers of this list do not recommend that email service administrators use this list to reject messages, or classify messages as spam, in an indiscriminate way.  The addresses in the list are carefully classified in a nuanced way, so the list must be consumed in a nuanced way.

## History ##

This project was started by email service providers in the higher education IT sector.  Students, faculty and staff have been targeted by phishing campaigns that convince them to reply to email messages with their personal information, most notably their email account password.

The phishers then use the stolen account credentials to send more phishing campaigns using the school's otherwise trustworthy email system.

The reply address of these phishing messages are usually fake accounts within legitimate email domains, such as live.com or yahoo.com.

# Download #

This is the list of reply addresses being used in phishing campaigns.

http://svn.code.sf.net/p/aper/code/phishing_reply_addresses

# List Removal #

This list contains email addresses reported to have been seen in
phishing attempts.  We provide data, but do not control how the list
is used.  If your email is blocked, please do not ask us for help.
Instead, you should contact the administrator of the site that is
blocking your email so that they are aware that they may not be using this list appropriately.

If you would like an address to be cleared from the list, send an email to:
[anti-phishing-email-reply-discuss@googlegroups.com](mailto:anti-phishing-email-reply-discuss@googlegroups.com)

# How to participate #

To subscribe to the mailing list, so that you can post new addresses, send an email to:
[anti-phishing-email-reply-discuss@googlegroups.com](mailto:anti-phishing-email-reply-discuss@googlegroups.com)

To submit additions to the list or updates to existing list entries, email
them to the mailing list in the format described in [Guidelines](Guidelines.md)