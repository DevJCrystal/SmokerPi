import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smoker Pi',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.amber,
      ),
      home: const MyHomePage(title: 'Smoker Pi'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final Future<SharedPreferences> _prefs = SharedPreferences.getInstance();

  Future<bool> findSmokerPi() async {
    final SharedPreferences prefs = await _prefs;
    // Search for the smoker pi
    // Check settings first for otherwise, check default smokerpi.local
    final String pi = (prefs.getString('pi') ?? "smokerpi.local");

    // Check the api for a response
    var url = Uri.http(pi, 'api/status');
    try {
      var response = await http.get(url);
      if (response.statusCode == 200) {
        return true;
      }
    } catch (e) {
      // TODO: Create better logging and error handling
      print("Error checking API: $e");
    }
    return false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
          IconButton(
              onPressed: () {
                // Launch Settings
              },
              icon: const Icon(Icons.settings))
        ],
      ),
      body: FutureBuilder(
        future: findSmokerPi(),
        builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
          // What to show while waiting for data
          if (!snapshot.hasData) return const CircularProgressIndicator();

          // What to show when there was an error connecting
          if (snapshot.data == false) {
            return const Center(
              child: Text("There was an error connecting to the Pi!"),
            );
          }
          // What to show when we are able to communicate
          return Center(
            child: Column(children: const [
              Text("Temp: 250"),
              Text("Graph here"),
            ]),
          );
        },
      ),
    );
  }
}
