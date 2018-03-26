Title: Calculate pi on Raspberry using Elixir
Date: 2018-03-14
Category: Elixir
Tags: raspberry-pi,elixir
slug: calculate-pi-on-raspberry-using-elixir

Elixir is a modern, functional programming language, based on the Erlang runtime
environment. Erlang has a long history of being a robust platform for building
distributed systems with many "processes" that run concurrently. The
processes in quotation marks means light-weight processing containers managed by
the BEAM (the Erlang runtime virtual machine), not actual operating system
processes.

During the last months I've dabbled a bit with Elixir, mostly from following the
excellent book by Dave Thomas: "Programming Elixir". By the way, the book will
soon be updated for Elixir version 1.6.

Since PI day is coming up (3/14 in U.S. date format), I thought it would be fun
to explore Elixir's concurrent processing to calculate some digits of the number
pi!

This article goes over the setup and some of the Elixir code. It is not intended
to be a Elixir tutorial. 

On the topic of "pi", why not use some Raspberry PIs ;-)


# Nodes on the network

My setup is four Raspberry Pi 3 devices. These four Raspberry Pis will each
run an instance of the BEAM (the Erlang VM), and these VM instances are called
"nodes". When these nodes are named, they can connect to other nodes.
Once connected, the nodes can send messages to processes running on other
nodes.  Apart from the four Raspberry Pi nodes, there is one more node in my
setup: the master node running on my laptop. This master node keeps track of
the work to be done and distributes work packets to the worker nodes.

Once a worker node connects to the master node, it sends the
"next_digit_positions" message to the master node. The master node sends back
the next 8 digit positions. The worker node calculates the value of each digit
position and sends an "update_pi" message with the result of the digit value.
The master node updates the value of pi. This process repeats until the target
number of digit positions have been calculated.

The graphic below illustrates the idea for work distribution:

![stack]({filename}/extras/master-worker.png)

# The Raspberry PIs

The company i work for (PMA Solutions) recently had a developer challenge, kind
of an internal hackathon, in which each team had to build a voice-interface
using Raspberry PI devices. So i could borrow two Raspberry Pis and with two of
my own I have a little stack of four devices connected to the local network via
Ethernet cables to a switch mounted under the desk:

![stack]({filename}/extras/rpi-stack.JPG)

Each device is a Raspberry Pi model B, having a 1.2 GHz 64-bit CPU which is
rather slow, but four cores that can come in handy for concurrent computation.

Running the final program on the Raspberry Pis shot up the temperature upward of
80 °C. For any long periods of calculation this cannot be good for the life of
the chips so I added some heatsinks:

![heatsink]({filename}/extras/rpi-heatsink.JPG)

The heatsinks really make a difference. Without the heatsinks, the idle
temperature was about 45°C and with heatsink it came down to 42°C. During full
load, the temperature would be about 82°C without heatsink. With heatsink and
active cooling with some fans, the temperature could be held between 50°C and
60°C.

Here is the setup with three fans, moving the air in one direction:

![fan setup]({filename}/extras/rpi-fan-setup.JPG)

# Formula for calculating Pi

When one starts to look into formulas for Pi, one enters a fascinating world of
mathematics. There are several formulas that are based on a summation of a
series of terms. In this exercise, the
[Bailey–Borwein–Plouffe](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula) formula was used:

![BBP Formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/af6bc360851499dd2ab2a90bee03fbe2040089d5)

Each term in this sum represents a digit in the k'th digit position. Although,
the digit position is not a decimal position, it is a hexadecimal position. For
the sum and the resulting value of pi, it makes no difference. The series can be
broken up into "chunks" that can be assigned as work packets for the worker
nodes.

# Some background on Elixir/Erlang processes

Before going further with the Elixir implementation, here is a high-level
overview of processes in Elixir/Erlang. Erlang uses processes to isolate units
of processing, allowing concurrent programming. Processes do not expose their
state and the way they interact with other processes is by passing messages to
another process.

When spawning a new Elixir/Erlang process, the result is a PID - a process
identifier. Other processes can then send messages to this PID.

In the example module below, a process is spawned that keeps track of a count,
that can be incremented or decremented, depending on the message passed to the
process:

    :::Elixir:::
    defmodule Counter do
      def start(initial_value) do
        spawn fn -> count(initial_value) end
      end

      def count(counter) do
        receive do
          {:add, number}
            ->  count(counter + number)
          {:subtract, number}
            ->  count(counter - number)
          {:value, sender}
            ->  send(sender, counter)
                count(counter)
        end
      end
    end

Calling the `start` function spawns a new process using the `spawn` function that
takes one argument: a function to run. In this case, the anonymous function
calls the `count` function that will wait for messages to be received.

The `count` function contains a `receive do` block. It will match an incoming
message value and act on it. In each of the three types of messages, the count
function calls itself again. This is often called a "receive loop" because the
function will keep on listening for new messages and respond to them. Note: this
is not your typical recursion that creates a new call stack on each function
call.  Elixir uses "tail call optimization" when the recursive function call is
the last statement executed in the function body. In that case the call stack is
not kept around when the function is called again, so there is no stack
overflow.

Elixir does not have the concept of objects that carry state with them. In this
case we do want to keep track of the counter value. The state is passed to the
count function as an argument.

Below is a sample of how the above Counter module can be used:

    :::Elixir:::
    # Create a new Counter process, and
    # initialize the counter to 10:
    pid = Counter.start(10)

    # Add 5 and subtract 3 from the
    # counter by sending messages to
    # the process's process id:
    send(pid, {:add, 5})
    send(pid, {:subtract, 3})

    # Send a message to retrieve
    # the value of the counter. Here we
    # send the current process's pid
    # (the result of calling self()),
    # and that way the Counter can send
    # back the value
    send(pid, {:value, self()})

    # Finally, receive the message with
    # the value and print to the console:
    receive do
      value -> IO.puts "Value is #{value}"
    end

Erlang comes with a whole framework for managing processes, called OTP - the
Open Telecom Platform. One of the constructs that encapsulates the process
communication and message passing is the GenServer, a generic server that can
respond to synchronous and asynchronous calls. For each type of call, the
GenServer manages the state. It takes care of the receive loops. The Counter can
be written as follows to be a GenServer:

    :::Elixir:::
    defmodule Counter do
      use GenServer

      def handle_cast({:add, number}, counter) do
        # Cast does not have a reply.
        # State changes by adding number:
        {:noreply, counter + number}
      end

      def handle_cast({:subtract, number}, counter) do
        # Cast does not have a reply.
        # State changes by subtracting number:
        {:noreply, counter - number}
      end

      def handle_call(:value, _from, counter) do
        # A call is synchronous and returns a value.
        # The three-part tuple below indicates that
        # - a value is to be returned
        # - the return value is `counter`
        # - the state `counter` (unchanged)
        {:reply, counter, counter}
      end
    end

In this example, the Counter GenServer accepts "cast" (asynchronous) and "call"
(synchronous) invocations. The above example has two `handle_cast` function
definitions. One of these two will be called, based on pattern matching the
first argument. The `handle_cast` function is a callback that Elixir will call
when it receives a `GenServer.cast` function call. Similarly, there is a
`handle_call` callback defined that will handle calls to `GenServer.call`. The
difference between `GenServer.cast` and `GenServer.call` is that a cast is
asynchronous - it does not return a value to the caller - hence the `:noreply`
atom. The call on the other hand is synchronous and returns a value.

Here is an example of using the Counter as a GenServer:

    :::Elixir:::
    # Create a new Counter GenServer,
    # and initialize the counter to 10:
    {:ok, pid} = GenServer.start_link(Counter, 10)

    # Add 5 and subtract 3 from the counter by
    # sending messages to # the process's pid
    GenServer.cast(pid, {:add, 5})
    GenServer.cast(pid, {:subtract, 3})
    value = GenServer.call(pid, :value)
    IO.puts "The value is #{value}"

# The master node

One node is designated the "master node". It runs a GenServer that defines a
list of digit positions from 0 to 10000, and keeps track of the value of pi
computed so far.

To calculate pi to many decimal places, one cannot simply use floating point
data types. In this project, the Elixir [Decimal module](https://hexdocs.pm/decimal)
was used, which handles arbitrary precision numeric values.

Here is the Elixirpi.Collector module, somewhat simplified compared to the
version on [GitHub](https://github.com/pythonquick/elixirpi):

    :::Elixir:::
    defmodule Elixirpi.Collector do
      use GenServer
      alias Decimal, as: D
      @digit_batch_size 8
      @target_hex_digits 10000
      @precision div(@target_hex_digits * 4, 3)

      def start do
        digit_positions = Enum.reduce(@target_hex_digits..0, [], &([&1 | &2]))
        pi = D.new(0) # Initial value
        {:ok, pid} = GenServer.start_link(__MODULE__, {pi, digit_positions})
        :global.register_name(:collector_process_name, pid)

        # Serve worker requests - do not exit
        :timer.sleep(:infinity)
      end

      ##############################################################################
      # GenServer callbacks
      ##############################################################################

      def handle_call(:next_digit_positions, _from, {pi, digit_positions}) do
        {next_digits, remaining}  = Enum.split(digit_positions, @digit_batch_size)
        output_progress(next_digits, pi)
        {:reply, {next_digits}, {pi, remaining}}
      end

      def handle_cast({:update_pi, additional_term}, {pi, digit_positions}) do
        D.set_context(%D.Context{D.get_context | precision: @precision}) 
        updated_pi = D.add(pi, additional_term)
        {:noreply, {updated_pi, digit_positions}}
      end

      # ... a few more private functions omited
    end

In the `start` function, the `Enum.reduce` function takes each item of the range
(10000..0) and successively adds it to the accumulator construct, which is
initially the empty list: []:

    :::Elixir:::
    digit_positions = Enum.reduce(@target_hex_digits..0, [], &([&1 | &2]))

This results in a list of integer values from 0 up to 10000 inclusive. 

The server process is created in the following line using the function
`GenServer.start_link`. Here we initialize the state of the GenServer with two
items:

* the value of pi calculated so far
* the list of digit positions for the number pi to be calculated, 

Note: the PID of the master node is registered in a global registry:

    :::Elixir:::
    :global.register_name(:collector_process_name, pid)

This way, other nodes can look up the PID of the master node, even if they are
on a different host on the network.


# The worker node

When each worker node starts up, it keeps asking the master node for more digits
to calculate. It calculates the digit positions in parallel task processes, and
sends back the results to the master node.

Here is a simplified module listing of the worker node:

    :::Elixir:::
    defmodule Elixirpi.Worker do
      alias Elixirpi.Collector
      alias Decimal, as: D

      # Commonly used formula constants:
      @d1 D.new(1)
      @d2 D.new(2)
      @d4 D.new(4)
      @d5 D.new(5)
      @d6 D.new(6)
      @d8 D.new(8)
      @d16 D.new(16)

      def term(digit_position) do
        D.set_context(%D.Context{D.get_context | precision: precision})
        sixteen_power = calc_sixteen_power(digit_position)
        digit_position_decimal = D.new(digit_position)
        eight_times_digit_pos = D.mult(@d8, digit_position_decimal)

        # Return the pi value at the digit position, according to the BBP formula:
        D.div(@d4, eight_times_digit_pos |> D.add(@d1))
        |> D.sub(D.div(@d2, eight_times_digit_pos |> D.add(@d4)))
        |> D.sub(D.div(@d1, eight_times_digit_pos |> D.add(@d5)))
        |> D.sub(D.div(@d1, eight_times_digit_pos |> D.add(@d6)))
        |> D.div(sixteen_power)
      end

      def process_next_digits(precision) do
        D.set_context(%D.Context{D.get_context | precision: precision})

        # From master node, get the next set of digit positions to calculate:
        next_digit_positions = GenServer.call(master_node_pid(), :next_digit_positions)

        # Calculate each digit term in concurrent stream of Tasks:
        Task.async_stream(
            next_digit_positions,
            fn digit_position -> term(digit_position) end,
            timeout: 100000
        )
        |> Enum.each(fn {:ok, next_digit_term} ->
            # Send master node the value of each calculated digit position:
            GenServer.cast(master_node_pid(), {:update_pi, next_digit_term})
        end)

        next_digit_positions
      end

      def keep_processing_digits(precision) do
        next_digit_positions = process_next_digits(precision)
        case next_digit_positions do
            [] -> IO.puts "Worker finished"
            _ -> keep_processing_digits(precision)
        end
      end

      def run() do
        precision = Collector.precision
        keep_processing_digits(precision)
      end

      # ... a few more private functions omited

    end


In the `process_next_digits` function, it fetches the next chunk of digit
positions to calculate. Then, for each digit position, call `Task.async_stream`
to spawn a Task. A task is a process that runs a function in the background and
delivers a single result. Each task calculates a digit of pi using the `term`
function using the Bailey–Borwein–Plouffe formula mentioned above.

Finally, each of the task results are collected, and sent to the master node.

# The Result

The result of running the four Raspberry Pi nodes for two hours is the generated
file pi.txt with 10000 decimal digits. 

The goal was by no means to break any records with this. It is a fun way to
explore Elixir's (and Erlang's) programming model and how processes and nodes
can be distributed across the network to work with each other.

A next step can be to try a formula that converges faster to the value of pi.

The full module can be found in the [GitHub repository](https://github.com/pythonquick/elixirpi)

Happy pi day!

3.14159265358979323846264338327950288419
7169399375105820974944592307816406286208
9986280348253421170679821480865132823066
4709384460955058223172535940812848111745
0284102701938521105559644622948954930381
9644288109756659334461284756482337867831
6527120190914564856692346034861045432664
8213393607260249141273724587006606315588
1748815209209628292540917153643678925903
6001133053054882046652138414695194151160
9433057270365759591953092186117381932611
7931051185480744623799627495673518857527
2489122793818301194912983367336244065664
3086021394946395224737190702179860943702
7705392171762931767523846748184676694051
3200056812714526356082778577134275778960
9173637178721468440901224953430146549585
3710507922796892589235420199561121290219
6086403441815981362977477130996051870721
1349999998372978049951059731732816096318
5950244594553469083026425223082533446850
3526193118817101000313783875288658753320
8381420617177669147303598253490428755468
7311595628638823537875937519577818577805
3217122680661300192787661119590921642019
8938095257201065485863278865936153381827
9682303019520353018529689957736225994138
9124972177528347913151557485724245415069
5950829533116861727855889075098381754637
4649393192550604009277016711390098488240
1285836160356370766010471018194295559619
8946767837449448255379774726847104047534
6462080466842590694912933136770289891521
0475216205696602405803815019351125338243
0035587640247496473263914199272604269922
7967823547816360093417216412199245863150
3028618297455570674983850549458858692699
5690927210797509302955321165344987202755
9602364806654991198818347977535663698074
2654252786255181841757467289097777279380
0081647060016145249192173217214772350141
4419735685481613611573525521334757418494
6843852332390739414333454776241686251898
3569485562099219222184272550254256887671
7904946016534668049886272327917860857843
8382796797668145410095388378636095068006
4225125205117392984896084128488626945604
2419652850222106611863067442786220391949
4504712371378696095636437191728746776465
7573962413890865832645995813390478027590
0994657640789512694683983525957098258226
2052248940772671947826848260147699090264
0136394437455305068203496252451749399651
4314298091906592509372216964615157098583
8741059788595977297549893016175392846813
8268683868942774155991855925245953959431
0499725246808459872736446958486538367362
2262609912460805124388439045124413654976
2780797715691435997700129616089441694868
5558484063534220722258284886481584560285
0601684273945226746767889525213852254995
4666727823986456596116354886230577456498
0355936345681743241125150760694794510965
9609402522887971089314566913686722874894
0560101503308617928680920874760917824938
5890097149096759852613655497818931297848
2168299894872265880485756401427047755513
2379641451523746234364542858444795265867
8210511413547357395231134271661021359695
3623144295248493718711014576540359027993
4403742007310578539062198387447808478489
6833214457138687519435064302184531910484
8100537061468067491927819119793995206141
9663428754440643745123718192179998391015
9195618146751426912397489409071864942319
6156794520809514655022523160388193014209
3762137855956638937787083039069792077346
7221825625996615014215030680384477345492
0260541466592520149744285073251866600213
2434088190710486331734649651453905796268
5610055081066587969981635747363840525714
5910289706414011097120628043903975951567
7157700420337869936007230558763176359421
8731251471205329281918261861258673215791
9841484882916447060957527069572209175671
1672291098169091528017350671274858322287
1835209353965725121083579151369882091444
2100675103346711031412671113699086585163
9831501970165151168517143765761835155650
8849099898599823873455283316355076479185
3589322618548963213293308985706420467525
9070915481416549859461637180270981994309
9244889575712828905923233260972997120844
3357326548938239119325974636673058360414
2813883032038249037589852437441702913276
5618093773444030707469211201913020330380
1976211011004492932151608424448596376698
3895228684783123552658213144957685726243
3441893039686426243410773226978028073189
1544110104468232527162010526522721116603
9666557309254711055785376346682065310989
6526918620564769312570586356620185581007
2936065987648611791045334885034611365768
6753249441668039626579787718556084552965
4126654085306143444318586769751456614068
0070023787765913440171274947042056223053
8994561314071127000407854733269939081454
6646458807972708266830634328587856983052
3580893306575740679545716377525420211495
5761581400250126228594130216471550979259
2309907965473761255176567513575178296664
5477917450112996148903046399471329621073
4043751895735961458901938971311179042978
2856475032031986915140287080859904801094
1214722131794764777262241425485454033215
7185306142288137585043063321751829798662
2371721591607716692547487389866549494501
1465406284336639379003976926567214638530
6736096571209180763832716641627488880078
6925602902284721040317211860820419000422
9661711963779213375751149595015660496318
6294726547364252308177036751590673502350
7283540567040386743513622224771589150495
3098444893330963408780769325993978054193
4144737744184263129860809988868741326047
2156951623965864573021631598193195167353
8129741677294786724229246543668009806769
2823828068996400482435403701416314965897
9409243237896907069779422362508221688957
3837986230015937764716512289357860158816
1755782973523344604281512627203734314653
1977774160319906655418763979293344195215
4134189948544473456738316249934191318148
0927777103863877343177207545654532207770
9212019051660962804909263601975988281613
3231666365286193266863360627356763035447
7628035045077723554710585954870279081435
6240145171806246436267945612753181340783
3033625423278394497538243720583531147711
9926063813346776879695970309833913077109
8704085913374641442822772634659470474587
8477872019277152807317679077071572134447
3060570073349243693113835049316312840425
1219256517980694113528013147013047816437
8851852909285452011658393419656213491434
1595625865865570552690496520985803385072
2426482939728584783163057777560688876446
2482468579260395352773480304802900587607
5825104747091643961362676044925627420420
8320856611906254543372131535958450687724
6029016187667952406163425225771954291629
9193064553779914037340432875262888963995
8794757291746426357455254079091451357111
3694109119393251910760208252026187985318
8770584297259167781314969900901921169717
3727847684726860849003377024242916513005
0051683233643503895170298939223345172201
3812806965011784408745196012122859937162
3130171144484640903890644954440061986907
5485160263275052983491874078668088183385
1022833450850486082503930213321971551843
0635455007668282949304137765527939751754
6139539846833936383047461199665385815384
2056853386218672523340283087112328278921
2507712629463229563989898935821167456270
1021835646220134967151881909730381198004
9734072396103685406643193950979019069963
9552453005450580685501956730229219139339
1856803449039820595510022635353619204199
4745538593810234395544959778377902374216
1727111723643435439478221818528624085140
0666044332588856986705431547069657474585
5033232334210730154594051655379068662733
3799585115625784322988273723198987571415
9578111963583300594087306812160287649628
6744604774649159950549737425626901049037
7819868359381465741268049256487985561453
7234786733039046883834363465537949864192
7056387293174872332083760112302991136793
8627089438799362016295154133714248928307
2201269014754668476535761647737946752004
9075715552781965362132392640616013635815
5907422020203187277605277219005561484255
5187925303435139844253223415762336106425
0639049750086562710953591946589751413103
4822769306247435363256916078154781811528
4366795706110861533150445212747392454494
5423682886061340841486377670096120715124
9140430272538607648236341433462351897576
6452164137679690314950191085759844239198
6291642193994907236234646844117394032659
1840443780513338945257423995082965912285
0855582157250310712570126683024029295252
2011872676756220415420516184163484756516
9998116141010029960783869092916030288400
2691041407928862150784245167090870006992
8212066041837180653556725253256753286129
1042487761825829765157959847035622262934
8600341587229805349896502262917487882027
3420922224533985626476691490556284250391
2757710284027998066365825488926488025456
6101729670266407655904290994568150652653
0537182941270336931378517860904070866711
4965583434347693385781711386455873678123
0145876871266034891390956200993936103102
9161615288138437909904231747336394804575
9314931405297634757481193567091101377517
2100803155902485309066920376719220332290
9433467685142214477379393751703443661991
0403375111735471918550464490263655128162
2882446257591633303910722538374218214088
3508657391771509682887478265699599574490
6617583441375223970968340800535598491754
1738188399944697486762655165827658483588
4531427756879002909517028352971634456212
9640435231176006651012412006597558512761
7858382920419748442360800719304576189323
4922927965019875187212726750798125547095
8904556357921221033346697499235630254947
8024901141952123828153091140790738602515
2274299581807247162591668545133312394804
9470791191532673430282441860414263639548
0004480026704962482017928964766975831832
7131425170296923488962766844032326092752
4960357996469256504936818360900323809293
4595889706953653494060340216654437558900
4563288225054525564056448246515187547119
6218443965825337543885690941130315095261
7937800297412076651479394259029896959469
9556576121865619673378623625612521632086
2869222103274889218654364802296780705765
6151446320469279068212073883778142335628
2360896320806822246801224826117718589638
1409183903673672220888321513755600372798
3940041529700287830766709444745601345564
1725437090697939612257142989467154357846
8788614445812314593571984922528471605049
2212424701412147805734551050080190869960
3302763478708108175450119307141223390866
3938339529425786905076431006383519834389
3415961318543475464955697810382930971646
5143840700707360411237359984345225161050
7027056235266012764848308407611830130527
9320542746286540360367453286510570658748
8225698157936789766974220575059683440869
7350201410206723585020072452256326513410
5592401902742162484391403599895353945909
4407046912091409387001264560016237428802
1092764579310657922955249887275846101264
8369998922569596881592056001016552563756

785
