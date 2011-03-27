#!/usr/bin/perl
use strict;
use warnings;
use FindBin;
use XML::TreePP;
use LWP::Simple;
use Template;
use CGI;
use DateTime;
use JSON::Syck;
use Cache::File;
use Data::Dumper;
use utf8;
my $cache = Cache::File->new(cache_root => '/tmp/cacheroot',
    lock_level => Cache::File::LOCK_LOCAL(),
    default_expires => '10 minutes');

my $cgi = CGI->new();

my $api = "http://tepco-usage-api.appspot.com/2011/3.json";
my $contents = $cache->get( $api );
my $source ;
if (!$contents){
    $source = "site";
    $contents = get($api);
    $cache->set( $api, $contents, '10 minutes' );
}else{
    $source = "cache";
}
my $obj = JSON::Syck::Load($contents);
my @out;
for my $item (@$obj){
    $item->{month} -= 1;
}


my $tt = Template->new({ INCLUDE_PATH => "$FindBin::RealBin/templates", }) || die $Template::ERROR, "\n";

my $vars = {
    source => $source,
    obj => $obj,
};
print $cgi->header(-type=>'text/html' , -charset=>'utf-8'); 
my $output = $tt->process('index.tt',$vars,"$FindBin::RealBin/index.html") || die $tt->error(), "\n";
#print $output;
#print Dumper($obj);
