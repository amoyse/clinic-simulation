
# Clinic Simulation ISS CW1

This project uses the dependencies listed in the requirements.txt file. Which can be installed by running the `config.sh` script:
```bash
./config.sh
```

As it is a simulation, much of the functionality of this application has not been implemented, or has been implemented to the bare minimum to display concepts, not provide the full functionality of the clinic's systems.

Keys are securely stored in the .env file, and everything should work after dependencies have been installed, by running:
```python
python3 run.py
```

---

There are currently 6 users set up. Each is called 'user1', 'user2' etc. and the password for each account is currently 'pass'.

#### User Roles
user1 = doctor

user2 = patient

user3 = patient

user4 = finance

user5 = admin

user6 = researcher

---

All of the data for the clinic is stored in MediCloud, including user data, and unstructured data contained in the `uploads` folder.
Authentication works through an SSO system, which queries the encrypted `users.json` file, decrypts it, then checks if the hashed input password matches the stored hash. If so, a JWT token is generated and stored in cookies. This allows the services to query this to see if the user has been authenticated.

RBAC has been implemented by the custom decorator in the decorators.py file in the `utils` folder.

Data requests sent from services to MediCloud are encrypted with AES, with the encryption key encrypted with RSA. For this, each service (including MediCloud) has a public and private key, with the public keys assumed to be shared with each other, stored in the `public_keys` folder. MediCloud then decrypts these requests by decrypting the AES key with the MediCloud private key, then gets the data needed from the encrypted database, and encrypts it with the key and sends it back.

File upload works, and files are encrypted and stored in the `uploads` folder, but I have not implemented proper retrieval of data. I have written a route to get data for a specific file, which is then decrypted, but I have not integrated this fully, as it is just a simulation.

