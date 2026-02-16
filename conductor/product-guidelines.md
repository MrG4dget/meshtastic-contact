# Product Guidelines - Meshtastic Contact

## Prose Style and Tone
- **Professional and Technical:** Communication should be precise, concise, and focused on clarity. We assume the user is familiar with Meshtastic terminology or is a power user looking for efficient control. Avoid unnecessary conversational filler in both the UI and documentation.

## Visual Identity and Messaging
- **Information Density:** The UI should prioritize high information density, acting as a functional dashboard for the Meshtastic node. Where possible, maximize the screen real estate to provide the user with as much relevant data as possible (mesh status, node list, telemetry, etc.) at a single glance.

## User Experience (UX) Principles
- **Keyboard-First Design:** Efficiency is paramount. Every feature and navigation element must be accessible via logical and consistent keyboard shortcuts. The user should be able to perform all management and communication tasks without needing to switch to a mouse.

## Design Constraints
- **Terminal Compatibility:** All UI elements must be compatible with standard terminal emulators and respect the constraints of the curses library.
- **Performance:** UI updates must be efficient to ensure responsiveness, especially when connected via low-bandwidth or high-latency serial/network links.
