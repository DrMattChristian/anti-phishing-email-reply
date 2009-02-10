#!/usr/bin/perl

# Written by rotaiv@gmail.com

# http://anti-phishing-email-reply.googlecode.com/svn/trunk/phishing_reply_addresses

$webfile = "/root/data/phishing_reply_addresses";
$aufile = "/root/data/phishing_exclude_au";
$accessfile = "/etc/mail/access";
$logfile = "/var/log/phishing.log";

# Current date & time in yyyy-mm-dd hh:mm:ss format
@dt=localtime(time);
$datetime=sprintf("%.4d-%.2d-%.2d %.2d:%.2d:%.2d",
 $dt[5]+1900,$dt[4]+1,$dt[3],$dt[2],$dt[1],$dt[0]);
$cdate=sprintf("%.4d/%.2d/%.2d",$dt[5]+1900,$dt[4]+1,$dt[3]);
$ctime=sprintf("%.2d:%.2d:%.2d",$dt[2],$dt[1],$dt[0]);

# -----------------------------------------------------------------------------
# Download phishing file
# -----------------------------------------------------------------------------

chdir "/root/data/";
$oldweb = `md5sum $webfile`;
unlink $webfile;
system("wget -q http://anti-phishing-email-reply.googlecode.com/svn/trunk/phishing_reply_addresses");
$newweb= `md5sum $webfile`;

# Abort if file not updated
if ($oldweb eq $newweb) {
 exit;
}

# Calculate hash for current access file
my $oldaccess = `md5sum $accessfile`;

# -----------------------------------------------------------------------------
# Read web file
# -----------------------------------------------------------------------------

open(WEBFILE,"<$webfile") || die "$!";

while($txt=<WEBFILE>) {
  # Ignore comments or lines without "@"
  next if $txt =~ '#';
  next if $txt !~ '@';
  @rec = split ',', $txt;
  $web{$rec[0]}=1;
}
close(WEBFILE);

# -----------------------------------------------------------------------------
# Read AU exclude file
# -----------------------------------------------------------------------------

open(AUFILE,"<$aufile") || die "$!";

while($txt=<AUFILE>) {
  # Ignore comments or lines without "@"
  next if $txt =~ '#';
  next if $txt !~ '@';
  chomp($txt);

  delete($web{$txt}) if exists($web{$txt});

}
close(AUFILE);

# -----------------------------------------------------------------------------
# Read access file
# -----------------------------------------------------------------------------

open(ACCESSFILE,"<$accessfile") || die "$!";

while($txt=<ACCESSFILE>) {

  # Ignore comments or lines without "@"
  next if $txt =~ '#';
  next if $txt !~ '@';

  # Look for reject lines
  next unless $txt =~ /^(.*)ERROR/;

  # Convert to lowercase and trim spaces
  $email=lc(rtrim($1));

  if (exists($web{$email})) {
    delete($web{$email});
  }
}
close(AUFILE);

# -----------------------------------------------------------------------------
# Add new addresses
# -----------------------------------------------------------------------------

open(ACCESSFILE,">>$accessfile") || die "$!";
open(LOGFILE,">>$logfile") || die "$!";

while(($email, $value) = each(%web)) {
  printf ACCESSFILE ("%-45s ERROR:\"550 Blocked by AU ITS\"\n", $email);
  print LOGFILE "$datetime,W,$email\n";
}
close(ACCESSFILE);
close(LOGFILE);

# -----------------------------------------------------------------------------
# Check if access file changed
# -----------------------------------------------------------------------------
$newaccess = `md5sum $accessfile`;
if ( $oldaccess ne $newaccess) {
  system("/sbin/service sendmail reload > /dev/null");
}


# =============================================================================
sub rtrim($)
# =============================================================================
{
  my $string = shift;
  $string =~ s/\s+$//;
  return $string;
}
