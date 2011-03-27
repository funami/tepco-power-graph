#!/usr/bin/perl
use strict;
use warnings;
use lib qw(/home/sedona/local/perl/lib/perl5/site_perl/5.8.9/mach /home/sedona/local/perl/lib/perl5/site_perl /home/sedona/local/perl/lib/perl5/5.8.9/mach /home/sedona/local/perl/lib/perl5);
use FindBin;
use LWP::Simple;
use Template;
use CGI;
use DateTime;
use JSON::Syck;
use Cache::File;
use Data::Dumper;
#use utf8;
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
my $g = "https://chart.googleapis.com/chart?chs=250x100&chd=t:60,40&cht=p3&chl=Hello|World";
my $i;
for my $item (@$obj){
    if ($item->{saving}){
        $item->{"save".$item->{saving}} = 4000;
        $item->{save} = "'計画停電実施'";
        $item->{saving} = "'".$item->{hour}."時'";
    }else{
        $item->{save} = 'undefined';
        $item->{saving} = 'undefined';
    }
    $item->{month} -= 1;
    $item->{percent} = $item->{usage}/$item->{capacity};
}


my $tt = Template->new({ INCLUDE_PATH => "$FindBin::RealBin/templates", }) || die $Template::ERROR, "\n";

my $b = pop(@$obj);
my $vars = {
    source => $source,
    obj => $obj,
    g => $g,
    b => $b,
    now => DateTime->now(time_zone=>'Asia/Tokyo'),
};
my $output = $tt->process('index.tt',$vars,"$FindBin::RealBin/index.html") || die $tt->error(), "\n";
print $cgi->redirect('http://rss.rdy.jp/tepco/index.html');
#$tt->process('index.tt',$vars) || die $tt->error(), "\n";
#print Dumper($obj);
