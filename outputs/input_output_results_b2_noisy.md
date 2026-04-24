# Input To Requirements Results

System: `B2 keyword-normalized baseline on noisy pilot dialogues`

This file shows exactly what was fed into the system and the requirements it produced.

## manual_001_amazing_lunch_indicator_noisy

- Domain: `restaurant_discovery`
- Split: `train`
- Source dataset: `software_requirements_dataset`
- Source document: `c01_amazing_lunch_indicator`

### Input Dialogue

- `1` `bot`: What kind of system do you want?
- `2` `user`: Basically a phone app for finding food spots near me and checking what each place offers.
- `3` `bot`: Who will use it?
- `4` `user`: Regular app users, restaurant people using the portal, and whoever manages the whole thing.
- `5` `bot`: What should users be able to do?
- `6` `user`: People should be able to look up places to eat, bounce between map and list results, open the full place details, and get directions. The restaurant side should update venue info, and management should approve those restaurant accounts.
- `7` `bot`: Do users need login or authentication?
- `8` `user`: Yeah, the mobile side needs sign-in, and the portal side needs accounts too for the restaurant side and the people running it.
- `9` `bot`: Are there performance requirements?
- `10` `user`: Searches need to feel quick, like two seconds tops, and if GPS or the internet dies the app should say so instead of just hanging.
- `11` `bot`: Are there security requirements?
- `12` `user`: Login traffic needs protecting, and after three bad tries the portal account should cool off for about thirty minutes.

### Output Functional Requirements

- `FR1` The system shall support authentication using mobile app username/password login and web portal username/password login.
- `FR2` The system shall allow users to search for restaurants using multiple search options.
- `FR3` The system shall allow users to view restaurant results in map and list views.
- `FR4` The system shall allow users to open detailed restaurant information pages.
- `FR5` The system shall allow users to navigate to a selected restaurant using GPS.
- `FR6` The system shall allow restaurant owners to manage restaurant information through the web portal.
- `FR7` The system shall allow administrators to verify restaurant owners.

### Output Non-Functional Requirements

- `NFR1` `performance` The system shall return search results within 2 seconds.
- `NFR2` `performance` The system shall inform the user if internet or GPS connectivity is lost.
- `NFR3` `security` The system shall encrypt log-in communication messages.
- `NFR4` `security` The system shall disable restaurant owner and administrator log-in for 30 minutes after three failed attempts.

## manual_002_restaurant_menu_ordering_system_noisy

- Domain: `restaurant_ordering`
- Split: `dev`
- Source dataset: `software_requirements_dataset`
- Source document: `c07_restaurant_menu_ordering_system`

### Input Dialogue

- `1` `bot`: What kind of system do you want?
- `2` `user`: An in-restaurant ordering setup with table screens, staff tablets, and kitchen displays.
- `3` `bot`: Who will use it?
- `4` `user`: Diners, floor staff, kitchen crew, and managers.
- `5` `bot`: What should users be able to do?
- `6` `user`: Guests should send orders and buzz staff, servers should take cash or card payments, the kitchen needs to mark dishes ready, and managers should handle refunds.
- `7` `bot`: Do users need login or authentication?
- `8` `user`: Staff tablets need sign-in with usernames and passwords, but customers at the table screens should not have to log in.
- `9` `bot`: Are there performance requirements?
- `10` `user`: The backend should cope with at least two hundred connected devices, and it cannot drop live orders or payments.
- `11` `bot`: Are there security requirements?
- `12` `user`: The wireless side needs encryption, and a server should not be signed into multiple tablets at once.

### Output Functional Requirements

- `FR1` The system shall support authentication using tablet username/password login.
- `FR2` The system shall allow customers to place orders through an engaged menu.
- `FR3` The system shall allow customers to call for waiter assistance.
- `FR4` The system shall allow waiters to process cash and bankcard payments.
- `FR5` The system shall allow chefs to mark order items as ready to be served.
- `FR6` The system shall allow supervisors to issue refunds.

### Output Non-Functional Requirements

- `NFR1` `performance` The system shall support at least 200 concurrent device connections.
- `NFR2` `performance` The system shall preserve all active meals and orders without losing them.
- `NFR3` `performance` The system shall preserve all active customer payments without losing them.
- `NFR4` `security` The system shall encrypt wireless communication using SSLv3 and WPA2-PSK.
- `NFR5` `security` The system shall limit each waiter to one logged-in tablet at a time.
- `NFR6` `security` The system shall not require customers to log in on surface computers.

## manual_003_keepass_password_safe_noisy

- Domain: `password_management`
- Split: `test`
- Source dataset: `pure`
- Source document: `2008_keepass`

### Input Dialogue

- `1` `bot`: What kind of system do you want?
- `2` `user`: A password vault tool so people can keep account creds together safely.
- `3` `bot`: Who will use it?
- `4` `user`: Mostly regular users, plus IT admins in some cases.
- `5` `bot`: What should users be able to do?
- `6` `user`: They need to spin up and unlock encrypted vaults, find saved items, tweak entries, and move password data in or out.
- `7` `bot`: Do users need login or authentication?
- `8` `user`: Yep, access should rely on a master password, and maybe a key file too if they set up that combined key option.
- `9` `bot`: Are there performance requirements?
- `10` `user`: If someone copies a password, don't leave it sitting around in memory for more than ten seconds.
- `11` `bot`: Are there security requirements?
- `12` `user`: Everything should stay encrypted, the vault must not open without the needed master password or key file, and there should be no recovery backdoor.

### Output Functional Requirements

- `FR1` The system shall support authentication using master password, key file, and composite master key.
- `FR2` The system shall allow end users to create and open encrypted password databases.
- `FR3` The system shall allow end users to search stored entries.
- `FR4` The system shall allow end users to add and edit entries.
- `FR5` The system shall allow end users to import and export password data.

### Output Non-Functional Requirements

- `NFR1` `performance` The system shall keep copied passwords in memory for no more than 10 seconds.
- `NFR2` `security` The system shall store passwords in an encrypted database.
- `NFR3` `security` The system shall refuse to open a database without the required master password or key file.
- `NFR4` `security` The system shall provide no recovery password or backdoor for unlocking databases.

