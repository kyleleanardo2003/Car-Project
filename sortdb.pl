#!/usr/bin/perl


use strict;
use warnings;

# Check if a sort category is provided as a command-line argument
unless (@ARGV) {
    die "Usage: $0 <sort_category>\n";
}

# Extract the sort category from command-line
my $sort_category = shift @ARGV;

# Path to SQLite database file
my $db_file = "vehicle.db";

# Execute the SQLite query to fetch the data and print it sorted
system("sqlite3 $db_file <<EOF
.headers on
.mode column
SELECT * FROM Vehicle ORDER BY $sort_category;
EOF");

