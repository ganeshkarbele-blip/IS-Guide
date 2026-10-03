import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:math';

void main() {
  runApp(const BISElectricalApp());
}

class BISElectricalApp extends StatelessWidget {
  const BISElectricalApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BIS Electrical Standards Calculator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1E3A8A), // Deep Navy Blue
          primary: const Color(0xFF1E3A8A),
          secondary: const Color(0xFFD97706), // Amber
        ),
      ),
      home: const ElectricalCalculatorScreen(),
    );
  }
}

class ElectricalCalculatorScreen extends StatefulWidget {
  const ElectricalCalculatorScreen({Key? key}) : super(key: key);

  @override
  State<ElectricalCalculatorScreen> createState() =>
      _ElectricalCalculatorScreenState();
}

class _ElectricalCalculatorScreenState
    extends State<ElectricalCalculatorScreen> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    const ConduitSizingTab(),
    const CableDeratingTab(),
    const EarthingResistanceTab(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'BIS Electrical Standards Engine',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        backgroundColor: Theme.of(context).colorScheme.primary,
        elevation: 2,
      ),
      body: _pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (int index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.settings_input_hd),
            label: 'Conduit Fill',
          ),
          NavigationDestination(
            icon: Icon(Icons.flash_on),
            label: 'Cable Derating',
          ),
          NavigationDestination(
            icon: Icon(Icons.nature_people),
            label: 'Earthing (IS 3043)',
          ),
        ],
      ),
    );
  }
}

// ==========================================
// 1. CONDUIT SIZING TAB (IS 732 / IS 9537)
// ==========================================
class ConduitSizingTab extends StatefulWidget {
  const ConduitSizingTab({Key? key}) : super(key: key);

  @override
  State<ConduitSizingTab> createState() => _ConduitSizingTabState();
}

class _ConduitSizingTabState extends State<ConduitSizingTab> {
  int qty15 = 2;
  int qty25 = 2;
  int qty40 = 2;
  int bends = 0;

  int? recommendedConduitSize;
  double fillFactorPercent = 0.0;
  double totalCableArea = 0.0;

  // IS 694 single core cable areas (sq.mm)
  final Map<double, double> cableAreas = {
    1.5: 8.55,
    2.5: 12.57,
    4.0: 16.62,
  };

  // IS 9537 Part 3 conduit internal areas (sq.mm)
  final Map<int, double> conduitAreas = {
    16: 133.0,
    20: 224.0,
    25: 360.0,
    32: 607.0,
    40: 984.0,
    50: 1541.0,
  };

  void _calculateConduit() {
    double area = (qty15 * cableAreas[1.5]!) +
        (qty25 * cableAreas[2.5]!) +
        (qty40 * cableAreas[4.0]!);

    int totalCables = qty15 + qty25 + qty40;
    if (totalCables == 0) return;

    double permissibleFill = (totalCables == 1)
        ? 0.53
        : (totalCables == 2)
            ? 0.31
            : 0.40;

    double reqArea = area / permissibleFill;
    double bendDerating = (bends >= 2) ? pow(0.85, (bends ~/ 2)).toDouble() : 1.0;

    int? selected;
    for (var entry in conduitAreas.entries) {
      if ((entry.value * bendDerating) >= reqArea) {
        selected = entry.key;
        break;
      }
    }

    setState(() {
      totalCableArea = area;
      fillFactorPercent = permissibleFill * 100;
      recommendedConduitSize = selected;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            color: Colors.blue.shade50,
            child: const Padding(
              padding: EdgeInsets.all(12.0),
              child: Row(
                children: [
                  Icon(Icons.info_outline, color: Color(0xFF1E3A8A)),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'IS 732:2019 / IS 9537 Part 3 Conduit Fill Engine',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Color(0xFF1E3A8A)),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Cable Quantities (Single Core PVC IS 694):',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 10),
          _buildCounterRow('1.5 sq.mm Wires', qty15, (v) {
            setState(() => qty15 = v);
            _calculateConduit();
          }),
          _buildCounterRow('2.5 sq.mm Wires', qty25, (v) {
            setState(() => qty25 = v);
            _calculateConduit();
          }),
          _buildCounterRow('4.0 sq.mm Wires', qty40, (v) {
            setState(() => qty40 = v);
            _calculateConduit();
          }),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Number of 90° Bends:',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              DropdownButton<int>(
                value: bends,
                items: [0, 1, 2, 3, 4]
                    .map((e) => DropdownMenuItem(value: e, child: Text('$e Bends')))
                    .toList(),
                onChanged: (v) {
                  if (v != null) {
                    setState(() => bends = v);
                    _calculateConduit();
                  }
                },
              )
            ],
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF1E3A8A),
              minimumSize: const Size.fromHeight(50),
            ),
            onPressed: _calculateConduit,
            child: const Text('CALCULATE CONDUIT SIZE',
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(height: 24),
          if (recommendedConduitSize != null) _buildResultCard(),
        ],
      ),
    );
  }

  Widget _buildCounterRow(String label, int val, Function(int) onChange) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label),
        Row(
          children: [
            IconButton(
              icon: const Icon(Icons.remove_circle_outline),
              onPressed: val > 0 ? () => onChange(val - 1) : null,
            ),
            Text('$val', style: const TextStyle(fontWeight: FontWeight.bold)),
            IconButton(
              icon: const Icon(Icons.add_circle_outline),
              onPressed: () => onChange(val + 1),
            ),
          ],
        )
      ],
    );
  }

  Widget _buildResultCard() {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text('RECOMMENDED MMS CONDUIT SIZE',
                style: TextStyle(fontSize: 14, color: Colors.grey)),
            const SizedBox(height: 5),
            Text(
              '${recommendedConduitSize} mm',
              style: const TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFD97706)),
            ),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Total Cable Area:'),
                Text('${totalCableArea.toStringAsFixed(1)} sq.mm'),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Max Allowable Space Factor:'),
                Text('${fillFactorPercent.toInt()}%'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================
// 2. CABLE DERATING TAB (IS 732)
// ==========================================
class CableDeratingTab extends StatefulWidget {
  const CableDeratingTab({Key? key}) : super(key: key);

  @override
  State<CableDeratingTab> createState() => _CableDeratingTabState();
}

class _CableDeratingTabState extends State<CableDeratingTab> {
  double baseCurrent = 32.0;
  double ambientTemp = 45.0;
  double harmonicPercent = 20.0;

  final Map<int, double> tempFactors = {
    30: 1.00,
    35: 0.94,
    40: 0.87,
    45: 0.79,
    50: 0.71,
    55: 0.61,
  };

  double getSafeCapacity() {
    double tFactor = tempFactors[ambientTemp.toInt()] ?? 1.0;
    double hFactor = (harmonicPercent > 15) ? 0.86 : 1.0;
    return baseCurrent * tFactor * hFactor;
  }

  @override
  Widget build(BuildContext context) {
    double safeCapacity = getSafeCapacity();

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Base Current Rating (Amps):',
              style: TextStyle(fontWeight: FontWeight.bold)),
          Slider(
            value: baseCurrent,
            min: 10,
            max: 200,
            divisions: 38,
            label: '${baseCurrent.toInt()} A',
            onChanged: (v) => setState(() => baseCurrent = v),
          ),
          const SizedBox(height: 10),
          Text('Ambient Temperature: ${ambientTemp.toInt()} °C',
              style: const TextStyle(fontWeight: FontWeight.bold)),
          Slider(
            value: ambientTemp,
            min: 30,
            max: 55,
            divisions: 5,
            label: '${ambientTemp.toInt()} °C',
            onChanged: (v) => setState(() => ambientTemp = v),
          ),
          const SizedBox(height: 10),
          Text('Total Harmonic Distortion (THD): ${harmonicPercent.toInt()}%',
              style: const TextStyle(fontWeight: FontWeight.bold)),
          Slider(
            value: harmonicPercent,
            min: 0,
            max: 40,
            divisions: 8,
            label: '${harmonicPercent.toInt()}%',
            onChanged: (v) => setState(() => harmonicPercent = v),
          ),
          const SizedBox(height: 20),
          Card(
            color: Colors.amber.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  const Text('DERATED SAFE CURRENT CAPACITY',
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Text(
                    '${safeCapacity.toStringAsFixed(1)} Amps',
                    style: const TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1E3A8A)),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    'Standard: IS 732:2019 Table 3 & Annex S',
                    style: TextStyle(color: Colors.grey.shade700, fontSize: 12),
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}

// ==========================================
// 3. EARTHING RESISTANCE TAB (IS 3043)
// ==========================================
class EarthingResistanceTab extends StatefulWidget {
  const EarthingResistanceTab({Key? key}) : super(key: key);

  @override
  State<EarthingResistanceTab> createState() => _EarthingResistanceTabState();
}

class _EarthingResistanceTabState extends State<EarthingResistanceTab> {
  double soilResistivity = 100.0; // Ohm-m
  double pipeLength = 2.5; // meters
  double pipeDiameter = 50.0; // mm

  double calculatePipeResistance() {
    double lCm = pipeLength * 100;
    double dCm = (pipeDiameter / 1000) * 100;
    return (100 * soilResistivity / (2 * pi * lCm)) * log(4 * lCm / dCm);
  }

  @override
  Widget build(BuildContext context) {
    double resistance = calculatePipeResistance();
    bool isSafe = resistance <= 5.0;

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Soil Resistivity (Ohm-meter):',
              style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'e.g. 100 for clay, 500 for sand',
            ),
            onChanged: (v) {
              if (double.tryParse(v) != null) {
                setState(() => soilResistivity = double.parse(v));
              }
            },
          ),
          const SizedBox(height: 16),
          Text('Pipe Electrode Length: ${pipeLength} meters',
              style: const TextStyle(fontWeight: FontWeight.bold)),
          Slider(
            value: pipeLength,
            min: 1.5,
            max: 6.0,
            divisions: 9,
            label: '$pipeLength m',
            onChanged: (v) => setState(() => pipeLength = v),
          ),
          const SizedBox(height: 20),
          Card(
            color: isSafe ? Colors.green.shade50 : Colors.red.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  const Text('CALCULATED PIPE EARTH RESISTANCE',
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Text(
                    '${resistance.toStringAsFixed(2)} Ω',
                    style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: isSafe ? Colors.green.shade800 : Colors.red.shade800),
                  ),
                  const SizedBox(height: 5),
                  Text(
                    isSafe
                        ? '✔ Complies with IS 3043 safe limit (≤ 5.0 Ω)'
                        : '✘ Exceeds 5.0 Ω max threshold! Add parallel electrodes or soil treatment.',
                    style: TextStyle(
                        color: isSafe ? Colors.green.shade900 : Colors.red.shade900,
                        fontWeight: FontWeight.bold),
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
