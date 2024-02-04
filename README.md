This is not a full-featured app, it's a quick and dirty version.

The install script makes a lot of assumptions, and so does the actual executable.


- Create an A record with an IP address that you know isn't right (255.255.255.255 works)
- Clone into a directory
- Run install.sh
- Edit .env with AWS credentials, hosted zone ID, and DNS record name (with trailing dot)

