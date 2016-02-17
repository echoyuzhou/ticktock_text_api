# Backend interface to database of CoBot status, actions, etc.
# 
# [02-2-2012] [ming] - starting working on this using the previous BE (based on example of CMU myPOI system)
#

package TaskBE;

use ClientToCoBot;
############################################################
# This is the start-up routine, which also sets the command line options
############################################################
sub TaskBE::setCommandLineOptions {
	# get the arguments
	my @args = @_;
	print STDERR "setCommandLineoptions argument: @_ \n";
}

###############################
# send task info to CoBot
###############################

sub TaskBE::LoadRoomNumbers {
	# builds a hashtable. key: room number (e.g., 7221); value: room number with a prefix as required from CoBot side (e.g., F7221)
	$room_number_fn = shift;
	my %room_number_mapping = ();
	open MAP, "$room_number_fn" or die "cannot open location files\n";
	@lines = <MAP>;
	close(MAP);
	foreach my $l (@lines)
	{
		chomp;
		my @split_line = split(/,/,$l);
		my $room_number_full = $split_line[1];
		$room_number_full =~ m/[A-Z](\d+)/;
		my $room_number = $1;
		$room_number_mapping{$room_number} = $room_number_full;
	}
	return %room_number_mapping;
}

sub TaskBE::request {
	my $inputFrame_arg = shift;
	my %inputFrame = %$inputFrame_arg;
	my %outputFrame = ();
	my %room_number_mapping = LoadRoomNumbers("GHC7_locations2.txt");
	my $frame = ""; # message sent to CoBot
	my $queryType = $inputFrame{'query_type'};
	
	if ($queryType == 0)
	{
		print STDERR "Asking CoBot for interaction_start signal\n";
		my $recv_data = &ClientToCoBot::recv();
		#print STDERR "recv_data = $recv_data\n";
		if($recv_data eq "interaction_start")
		{
			print STDERR "CoBot sent an interaction_start signal\n";
			$outputFrame{"result.succeed"} = 1;
		}
		else
		{
			$outputFrame{"result.succeed"} = 0;
		}
	}
	
	elsif ($queryType == 1)
	{
		print STDERR "DeliverMsg Task\n";
		$frame = DeliverMsg(\%inputFrame,\%room_number_mapping);
		&ClientToCoBot::send($frame);
		$outputFrame{"result.succeed"} = 1;
	}
	elsif ($queryType == 2)
	{
		print STDERR "GoToRoom Task\n";
		$frame = GoToRoom(\%inputFrame,\%room_number_mapping);
		print $frame."\n";
		&ClientToCoBot::send($frame);
		$outputFrame{"result.succeed"} = 1;
	}
	elsif ($queryType == 3)
	{
		print STDERR "Escort Task\n";
		$frame = Escort(\%inputFrame,\%room_number_mapping);
		&ClientToCoBot::send($frame);
		$outputFrame{"result.succeed"} = 1;
	}
	elsif ($queryType == 5)
	{
		print STDERR "Interaction Status\n";
		$frame = InteractionStatus(\%inputFrame);
		&ClientToCoBot::send($frame);
		$outputFrame{"result.succeed"} = 1;
	}
	print STDERR "outputFrame = $frame\n";	
	
	$outputFrame{"result"} = "&STRUCT";
	print STDERR ">> " .$outputFrame{"result"}. "\n";
	  
	print STDERR "Output frame:\n";
	foreach my $k (keys %outputFrame) {
		printf STDERR "$k => ".$outputFrame{$k}."\n";
	}
	print STDERR "----------------------------------\n";
	return \%outputFrame;
	
}

sub DeliverMsg {
	#print STDERR "constructing DeliverMsg frame to CoBot ... \n";
	my $inputFrame_arg = shift;
	my %inputFrame = %$inputFrame_arg;
	my $room_number_arg = shift;
	my %room_number_mapping = %$room_number_arg;
	my $frame = "{'task_name':'DeliverMessage',"."'room':'".$room_number_mapping{$inputFrame{'msgdestination'}}."','user':'".$inputFrame{'sendername'}."','message':'".$inputFrame{'msg'}."','mid':100,'start_time':1,'end_time':100"."}";
	return $frame;
}

sub GoToRoom {
	#print STDERR "constructing GoToRoom frame to CoBot ... \n";
	my $inputFrame_arg = shift; 
	my %inputFrame = %$inputFrame_arg;
	my $room_number_arg = shift;
	my %room_number_mapping = %$room_number_arg;
	my $frame = "{'task_name':'GoToRoom',"."'room':'".$room_number_mapping{$inputFrame{'destination'}}."','mid':100,'start_time':1,'end_time':100"."}";
	return $frame;
}

sub Escort {
	#print STDERR "constructing Escort frame to CoBot ... \n";
	my $inputFrame_arg = shift;
	my %inputFrame = %$inputFrame_arg;
	my $room_number_arg = shift;
	my %room_number_mapping = %$room_number_arg;
	my $frame = "{'task_name':'Escort',"
	."'room1':'"
	.$room_number_mapping{$inputFrame{'escortorigin'}}
	."','room2':'"
	.$room_number_mapping{$inputFrame{'destination'}}
	."','obj':'"
	.$inputFrame{'visitorname'}
	."','mid':100,'start_time':1,'end_time':100"."}";
	return $frame;
}

# sending interaction(stop) message to CoBot - interaction in dialog ends
sub InteractionStatus {
	#print STDERR "constructing Interactin Status frame to CoBot ... \n";
	my $inputFrame_arg = shift;
	my %inputFrame = %$inputFrame_arg;
	
	my $frame = "{'message':'interaction_status','status':'interaction_stop','timestamp':'".$inputFrame{'time_stamp'}."'}";
	return $frame;
}

sub RoomNumberBindingFilter {
	# according to room number, add different prefix to the room number, as required by CoBot side.
	# e.g., F7224, O715
	# [2012-03-22] m: currently, we only deal with office numbers (F)
	my %number_prefix = shift; # key: prefix; value: a list of room numbers.

}
1;
