#!/usr/bin/perl
# 
# add-address-to-list.pl, DESCRIPTION
# 
# Copyright (C) 2008 Jesse Thompson
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# $Id:$
# Jesse Thompson <jesse.thompson@doit.wisc.edu>

use strict;
use warnings;

my $usage = "$0 user\@domain\nor\n$0 user\@domain,type,date\n";
my $list_file = "phishing_reply_addresses";
die "$list_file does not exist\n" unless ( -e $list_file );

my $new_entry = shift;
die $usage unless ( $new_entry );
my @entry_parts = split /,/, $new_entry;

unless ( $entry_parts[0] =~ m/^(.*@.*)$/ ) {
    die "invalid email address [$entry_parts[0]]\n";
}
$entry_parts[0] = lc $entry_parts[0];

if ( ! $entry_parts[1] ) {
    print "specify type: ";
    $entry_parts[1] = <>;
    chomp $entry_parts[1];
    if ( ! $entry_parts[1] ) {
        $entry_parts[1] = "A";
    }
}
unless ( $entry_parts[1] =~ m/^([ABCDE]+)$/ ) {
    die "invalid type [$entry_parts[1]]\n";
}

if ( ! $entry_parts[2] ) {
    print "specify date: ";
    $entry_parts[2] = <>;
    chomp $entry_parts[2];
    if ( ! $entry_parts[2] ) {
        my @time = localtime();
        $time[3] = sprintf("%02d",$time[3]);
        $time[4] = sprintf("%02d",++$time[4]);
        $time[5] += 1900;
        $entry_parts[2] = $time[5] . $time[4] . $time[3];
    }
}
unless ( $entry_parts[2] =~ m/^(\d{8})$/ ) {
    die "invalid type [$entry_parts[2]]\n";
}

my $tmp_list_file = $list_file.".tmp";
if ( -e $tmp_list_file ) {
    unlink $tmp_list_file or die "can't remove existing $tmp_list_file: $!\n";
}
open my $tmp_list_fh, ">", $tmp_list_file or die "can't open $tmp_list_file: $!\n";
open my $list_fh, "<", $list_file or die "can't open $list_file: $!\n";
my $entry_has_printed = 0;
my $entry_to_add = join ',', @entry_parts;
while ( <$list_fh> ) {
    my @current_entry = split ',', $_;
    if ( m/^#/ ) {
        print $tmp_list_fh $_;
    }
    elsif ( ! $entry_has_printed ) {
        if ( ($entry_parts[0] cmp $current_entry[0]) == 0 ) {
            if ( $current_entry[2] > $entry_parts[2] ) {
                $entry_parts[2] = $current_entry[2];
            }
            if ( ( $current_entry[1] cmp $entry_parts[1] ) != 0 ) {
                my @types = split //, $current_entry[1].$entry_parts[1];
                my %type_hash = ();
                foreach ( sort @types ) {
                    $type_hash{$_} = 1;
                }
                $entry_parts[1] = join '', sort keys %type_hash;
            }
            $entry_to_add = join ',', @entry_parts;
            print $tmp_list_fh $entry_to_add."\n";
            $entry_has_printed++;
        }
        elsif ( ($entry_parts[0] cmp $current_entry[0]) == -1 ) {
            print $tmp_list_fh $entry_to_add."\n";
            print $tmp_list_fh $_;
            $entry_has_printed++;
        }
        else {
            print $tmp_list_fh $_;
        }
    }
    else {
        print $tmp_list_fh $_;
    }
}
if ( ! $entry_has_printed ) {
    print $tmp_list_fh $entry_to_add."\n";
}
close $list_fh;
close $tmp_list_fh;

rename $tmp_list_file, $list_file or die "can't rename $tmp_list_file to $list_file: $!\n";
