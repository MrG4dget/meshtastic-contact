# Plan - Contact App Verification (Hardware)

## Phase 1: Environment & Connectivity Baseline
Verify that the hardware is recognized and the basic application loop can start.

- [x] Task: Hardware Presence Check - Ensure a Meshtastic node is connected and accessible via serial/USB. 051d533
- [x] Task: Application Boot - Start the `contact` app and verify the splash screen and initial UI state. a67ff91
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment & Connectivity Baseline' (Protocol in workflow.md)

## Phase 2: TUI Navigation & Stability
Navigate the interface to ensure all views are functional and responsive.

- [ ] Task: Menu Navigation - Cycle through Contact UI and Control UI menus; verify all sub-menus open correctly.
- [ ] Task: Dialog & Config Interaction - Open and close configuration dialogs to ensure no crashes occur during state changes.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: TUI Navigation & Stability' (Protocol in workflow.md)

## Phase 3: End-to-End Hardware Communication
Perform live transmission and reception tests using the physical mesh.

- [ ] Task: Transmission Test (TX) - Send a test message from the app and confirm it is broadcast by the local node.
- [ ] Task: Reception Test (RX) - Receive a message from a remote node and verify it appears correctly in the TUI message log.
- [ ] Task: Database Persistence - Verify that the sent/received messages are correctly stored in the SQLite database.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: End-to-End Hardware Communication' (Protocol in workflow.md)
