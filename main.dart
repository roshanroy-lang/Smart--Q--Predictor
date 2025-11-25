import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const API_BASE = String.fromEnvironment('API_BASE', defaultValue: 'http://10.0.2.2:8000');

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Queue Mobile',
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  State createState() => _HomeState();
}

class _HomeState extends State<HomePage> {
  int people = 0;
  int wait = 0;
  Timer? timer;
  bool loading=false;

  @override
  void initState() {
    super.initState();
    fetchData();
    timer = Timer.periodic(Duration(seconds:5), (_) => fetchData());
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  Future fetchData() async {
    setState(()=>loading=true);
    try {
      final res = await http.get(Uri.parse('$API_BASE/waiting-time'));
      if (res.statusCode == 200) {
        final d = json.decode(res.body);
        setState(()=>{ people = d['people_in_queue'] ?? 0, wait = d['estimated_wait_time_minutes'] ?? 0 });
      }
    } catch (e) {
      // ignore
    } finally {
      setState(()=>loading=false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Smart Queue')),
        body: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            children: [
              Text('People in queue', style: TextStyle(fontSize:18)),
              SizedBox(height:8),
              Text('\$people', style: TextStyle(fontSize:42, fontWeight: FontWeight.bold)),
              SizedBox(height:20),
              Text('Estimated wait (minutes)', style: TextStyle(fontSize:18)),
              SizedBox(height:8),
              Text('\$wait', style: TextStyle(fontSize:42, fontWeight: FontWeight.bold)),
              SizedBox(height:30),
              ElevatedButton(onPressed: fetchData, child: Text('Refresh')),
              if (loading) Padding(padding: EdgeInsets.only(top:10), child: CircularProgressIndicator()),
            ],
          ),
        )
    );
  }
}
