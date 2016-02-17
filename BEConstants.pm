# Backend interface to database of bus times, routes, etc.

# [05-21-2003] [antoine] - 
#
#

package BEConstants;

# query types
$Query_Where = 1;
$Query_HowFar = 2;
$Query_Category = 3;
$Query_Directions = 6;
#$Query_Multiple = 8;
# added by ming 6-14, 2011
# failure types
$OKAY = 0;
$INTERNAL_ERROR = 1;
