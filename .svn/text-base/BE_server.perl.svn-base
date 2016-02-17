#!/usr/bin/perl
use ClientToCoBot;
use Socket;
use TaskBE;
$SIG{'INT'} = \&cleanup;
$SIG{'KILL'} = \&cleanup;

# set the options
&TaskBE::setCommandLineOptions(@ARGV);

# initialize the service port
$servicePort = 23456;  # clients initially connect to us here

if (1) {
  # print out port, host info
  &status("servicePort: $servicePort");
}

# Watch a port for incoming frames
&tcp_server($servicePort);

# For debug: use a file instead of a network socket
#&tcp_stub("test.txt");

# close opened sockets
&cleanup;

exit(0);

#
# -- routines
#

sub usage {
    print "\n";
    print "\tusage: $0 [-h] [--servicePort <portnum>]\n";
    print "\n";
    print "\t       Dialogue Back-End Manager\n";
    print "\n";
    exit(-1);
}

sub tcp_stub {
    open(ClientSocket, $_[0]);
    &processFrame();
}


sub tcp_server {
    my ($servicePort) = $_[0];	
    my $sockaddr = 'S n a4 x8';
    my ($name, $aliases, $proto) = getprotobyname('tcp');
    ($name, $aliases, $servicePort) = getservbyname($servicePort, 'tcp')
	unless $servicePort =~ /^\d+$/;
    
    my $this = pack($sockaddr, AF_INET, $servicePort, "\0\0\0\0");
    print STDERR "tcp_server function...\n";
    for (;;) {
		socket(InitialConnectSocket, PF_INET, SOCK_STREAM, $proto) 
		    || die "socket: $!";
		setsockopt(InitialConnectSocket, SOL_SOCKET, SO_REUSEADDR, pack("l", 1)) 
			|| die "setsockopt: $!";
	
		bind(InitialConnectSocket, $this) || die "bind: $!";
		listen(InitialConnectSocket, 5) || die "connect: $!";
	
		select(InitialConnectSocket); 
		$| = 1; select(stdout);

		&status("Server accepting connection on port $servicePort");

		if (!($addr = accept(ClientSocket,InitialConnectSocket))) {
			die $!;
		} else {
			close InitialConnectSocket;

			select(ClientSocket); 
			$| = 1; select(stdout);

			my ($af, $subPort, $inetaddr) = unpack($sockaddr,$addr);
			@inetaddr = unpack('C4',$inetaddr);
			&status("Client accepted: ".join(".", @inetaddr)." $subPort");

			&processFrame();

		}
    }
}

sub processFrame {
	&status("processing frame ...");
    $/ = "\012" if $^O eq "MacOS";
    my $result; my $line; 
    my %framehash;
    my %resultFrame;
    my $bc=0; # bracket counter
    my @tokens=();
    while ($line = <ClientSocket>) {
	chomp($line);
	$valid = 0;
	$line =~ s/[^\w\d\{\}\s\t]+$//; # sanity
	#print STDERR "line";
	#print STDERR $line;
	if (lc($line) eq "quit") {
	    $valid = 1;
	    close(ClientSocket);
	    last;
	}

	if ($line =~ /\{/) {
	    # starting a new frame
	    # divide the input into tab- and newline-separated tokens 
	    # and check that it is a well-formed frame (as many '{' as '}')
	    $bc = 1;     
	    @tokens = ();
    	    $line =~ s/(^[\s\t]+|[\s\t]$)//; # removes trailing tabs
		print STDERR "The line after removing trailing tabs\n";
		print STDERR $line."\n";
		print STDERR "The line printed\n";
	    push(@tokens, split( /[\s\t]+/,$line, 2));       # pushes the tokens of the first line

	    print "INPUT:\n";

	    my $done = 0;
	    while (!$done and $line = <ClientSocket>) {
		chomp($line);

		print "$line\n";

    	        $line =~ s/(^[\s\t]+|[\s\t]$)//; # removes trailing tabs 	        

		push(@tokens, split(/[\s\t]+/,$line, 2));   # pushes the tokens of this line

	        if ($line !~ /\S/) {
 	           # skips blank lines
	           next;
	        }
	        elsif ($line =~ /\{/) {
	            # beginning of an embedded structure
		    $bc++;
 	        }
	        elsif ($line =~ /\}/) { 
		    $bc--;
		    if ($bc == 0) {
		        # all opened braces have been closed: end of the frame
		        $valid = 1;
		        $done = 1;
		    }
	        } 
	    }
		    
	

	    if ($valid) {
		# builds a hashtable from the tokens
        	%framehash = parseFrame(@tokens);
	
		# send the frame to the task-specific backend and gets the result
		$resultFrame = &TaskBE::request(\%framehash);

		# converts the result hashtable into a text-format frame
		$result = &buildTextFrame( $resultFrame);

		print "OUTPUT:\n$result\n";
		$valid = 1;

	    } else {
		$result = "** malformed frame";
	    }
	    
	}
	
	if (!$valid) {
	    if ($line =~ /\S/) {
		# received text that is neither a well-formed frame nor a blank line: fail
		$line =~ s/\n//;
		print ClientSocket "** unknown command: $line\n";
		&status("command $line failed: unknown command");
	    } 
	} else {
	    # sends the text-format result frame through the socket
	    print ClientSocket "$result";
	}

	print $prompt;
   }
}

sub cleanup {
    print ClientSocket "server quit\n";
    
    close ClientSocket if ClientSocket;
    close InitialConnectSocket if InitialConnectSocket;
    
    &status("received signal; exiting");
    exit(-1);
}

sub status {
    my $arg = $_[0];
    print STDERR "[ $arg ]\n";
}

# parsing utilties
#
sub parseFrame {
    local %framehash;
    local @tokens = @_;
	print STDERR @tokens;
	print STDERR "PASING THE FRAME...\n";
    #if ( ( shift(@tokens) ne "{" ) or ( pop(@tokens) ne "}" ) ) {
      #  warn "frame should start with '{' and end with '}'";
		#%framehash = '{' + %framehash;
		
    #}
  
    while (@tokens) {
        my $slotname = getSlotName("");
		print STDERR "$slotname \n";
        $framehash{$slotname} = getValue($slotname . '.');
		#$framehash{$slotname} = ($framehash{$slotname});
		#$framehash{$slotname} = ($framehash{$slotname});
		$framehash{$slotname} = substr $framehash{$slotname}, 1, -1;
		#$framehash{$slotname} = substr($framehash{$slotname},-1);
		print STDERR "$framehash{$slotname}\n";
    } 
	
    return %framehash;
}
  
# returns the next token from the text frame "as is" (without trying to recursively expand it)
sub getSlotName {
    return $_[0] . shift(@tokens);    # append to current scope string
}

# parses a value from the text frame
sub getValue {
    my $prefix = $_[0];
    my $token = shift(@tokens);

    if ( $token eq "{" ) {            # value is a structure
        # recursively analyzes the fields of the structure
        while ( $tokens[0] ne '}' ) {      
            my $slotname = getSlotName($prefix);
            $framehash{$slotname} = getValue($slotname . '.');
	    print "$slotname   ==>   $framehash{$slotname}\n";
        }
	shift(@tokens);

        return "&STRUCT";             # the value of a struct is always &STRUCT
    } 

    elsif ( $token =~ m/^:\d+/ ) {    # value is an array
        my $num;
        ($num) = $token =~ m/(\d+)/;
        if ( shift(@tokens) ne '{' ) {
            warn "Array $prefix should begin with a '{'";
            return "NO VALUE";
        }

        for ( my $i = 0; $i < $num; $i++ ) {
            if ( @tokens ) {
               $framehash{$prefix . "$i"} = getValue($prefix . "$i.");
            }
            else {
               return "NO VALUE";
            }
        }

        if ( (my $ending = shift(@tokens)) ne '}' ) {
            warn "Array $prefix should end with a '}', not $ending";
            print @tokens[0..3], "\n";
            return "NO VALUE";
        }
        return "&ARRAY[$num]";        # return &ARRAY[number_of_elements]
    }

    elsif(!($token eq "")) {                # value is an irreducible
        return $token;
    }

    return "NO VALUE";
}

# Returns a text frame from a given hashtable
sub buildTextFrame {
  my $hashframe_arg = $_[0];
  local %hashframe = %$hashframe_arg;
  local %structs = ();
  local %toplevel = ();

  # determines which tokens point to structures, which to arrays and which to atomic slots
  while (($k,$v) = each(%hashframe)) {

    if ($hashframe{$k} =~ /&ARRAY\[(\d+)\]/) {
      # creates an array and sets its structs to 
      # its number of elements
	  $structs{$k} = $1;
	}
	elsif ($hashframe{$k} eq "&STRUCT") {
	  # creates an empty structure
	  if (!defined $structs{$k}) {
	    $structs{$k} = "";
	  }
	}

    if (($k =~ /^(.+)\.([^\.]+)$/)&&($hashframe{$1} eq "&STRUCT")) {
	  # current tokoen is a field of a structure
	  # updates parent structure's list of fields
	  if ($structs{$1}) {
	    $structs{$1} .= ":".$2;                        
	  }
	  else {
	    $structs{$1} .= $2;                        
	  }
    }
    elsif ($k !~ /\./) {
	  # token do not contain any '.' => it is a toplevel token
	  $toplevel{$k}=1;
    }
  }

  # recursively gets the string representation of each token
  $result = "{\n";
  while (($k,$v) = each(%toplevel)) {
    $result .= hashToText( "\t", $k);
  }
  $result .= "}\n";

  return $result;
            
}

sub hashToText {
    my $indent = shift;			# leading tabs for indentation
    my $token = shift;			# token to be converted
    my $ret_string = "";

    if ($token =~ /(^|\.)\d+$/) {
	# token is a number: it is an array index => only returns the slot value
       	$ret_string = "$indent";
    }
    elsif ($token =~ /(^|\.)([^\.]+$)/) {
       # returns the string "token     value"
       $ret_string = "$indent$2\t";
    }

    # atomic token
    if (!defined $structs{$token}) {
        $ret_string .= "$hashframe{$token}\n";
    }
    # array token
    elsif ($hashframe{$token} =~ /^&ARRAY\[(\d+)\]$/) {
        my $n_elem = $1;
        $ret_string .= ":$n_elem\n$indent\{\n";
        for (my $i = 0; $i < $n_elem; $i++) {
	  $ret_string .= hashToText($indent."\t", $token.".".$i);	    
        }    
        $ret_string .= "$indent\}\n";
    }
    # structure token
    elsif ($hashframe{$token} eq "&STRUCT") {
	$ret_string .= "{\n";
	my @fields = split(/:/, $structs{$token});
	my $f;
	foreach $f (@fields) {
	    $ret_string .= hashToText($indent."\t", $token.".".$f);
	}
	$ret_string .= "$indent}\n";
    }
 
    return $ret_string;
}
