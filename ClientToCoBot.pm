package ClientToCoBot;
use IO::Socket;

sub send {
	my $send_data = shift;
	print "send data is $send_data\n";
	my $socket = new IO::Socket::INET (
		#PeerAddr  => '127.0.0.1', # local setting, sender
		#PeerPort  =>  19901, # local setting, sender
		#PeerAddr => '128.2.214.36', # Speech Lab
		#PeerPort => 5001, # Speech Lab
		#PeerAddr => '128.237.224.32', # Cobot1
		#PeerPort => 5001, # Cobot1
		PeerAddr => '128.237.255.247', # Cobot2
		PeerPort => 5001, # Cobot2
		Proto => 'tcp',
	)
	or die "Couldn't connect to Server\n";

	$socket->send($send_data);
	close($socket);
}

sub recv{
	print STDERR "socket recv ... \n";
	my $recv_data = "";
	my $socket = new IO::Socket::INET (
		#PeerAddr  => '127.0.0.1',  #local setting, reciver
		#PeerPort  =>  19902, #local setting, reciver
		#PeerAddr => '128.2.214.36', # Speech Lab
		#PeerPort => 5015, # Speech Lab
		#PeerAddr => '128.237.224.32', # Cobot1
		#PeerPort => 5015, #Cobot1
		PeerAddr => '128.237.255.247', # Cobot2
		PeerPort => 5015, #Cobot2
		Proto => 'tcp',
	)
	or die "Couldn't connect to Server\n";
	print STDERR "connection established\n";
	$socket->recv($recv_data,1024);
	print STDERR "recv = $recv_data\n";
	close($socket);
	return $recv_data;
}

1;
