const express = require('express');
const admin = require('firebase-admin');
const bodyParser = require('body-parser');

const app = express();

// Middleware untuk menguraikan data JSON dalam permintaan
app.use(express.json());

// Konfigurasi admin SDK Firebase
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

// Rute register
app.post('/register', (req, res) => {
  const { nama, username, email, password } = req.body;

  // Mengambil referensi ke koleksi "users" dalam Firestore
  const usersCollection = admin.firestore().collection('users');

  // Mengecek apakah email sudah digunakan
  usersCollection
    .where('email', '==', email)
    .get()
    .then((snapshot) => {
      if (!snapshot.empty) {
        res.status(400).json({ message: 'Email already in use' });
      } else {
        // Membuat data pengguna baru
        const newUser = { nama, username, email, password };

        usersCollection
          .add(newUser)
          .then(() => {
            res.status(200).json({ success: true, message: 'User registered successfully' });
          })
          .catch((error) => {
            res.status(500).json({ success: false, message: 'Error registering user' });
          });
      }
    })
    .catch((error) => {
      res.status(500).json({ success: false, message: 'Error registering user' });
    });
});


// Rute login
app.post('/login', (req, res) => {
  const { email, password } = req.body;

  // Mengambil referensi ke koleksi "users" dalam Firestore
  const usersCollection = admin.firestore().collection('users');

  // Mengecek apakah email dan password valid
  usersCollection
    .where('email', '==', email)
    .get()
    .then((snapshot) => {
      if (!snapshot.empty) {
        const user = snapshot.docs[0].data();
        if (user.password === password) {
          res.status(200).json({ success: true, message: 'Login successful' });
        } else {
          res.status(401).json({ success: false, message: 'Invalid credentials' });
        }
      } else {
        res.status(404).json({ success: false, message: 'User not found' });
      }
    })
    .catch((error) => {
      res.status(500).json({ success: false, message: 'Error logging in' });
    });
});

// Rute untuk menyimpan budget
app.post('/budget', (req, res) => {
  const { userId, budgetAmount } = req.body;

  // Mengambil referensi ke dokumen pengguna dalam Firestore
  const userDoc = admin.firestore().collection('users').doc(userId);

  // Mengupdate data budget pengguna
  userDoc
    .set({ budget: budgetAmount }, { merge: true })
    .then(() => {
      res.status(200).json({ message: 'Budget saved successfully' });
    })
    .catch((error) => {
      res.status(500).json({ message: 'Error saving budget' });
    });
});

// Rute untuk mendapatkan budget
app.get('/budget/:userId', (req, res) => {
  const userId = req.params.userId;

  // Mengambil referensi ke dokumen pengguna dalam Firestore
  const userDoc = admin.firestore().collection('users').doc(userId);

  // Mendapatkan data pengguna dan budget
  userDoc
    .get()
    .then((doc) => {
      if (doc.exists) {
        const userData = doc.data();
        const budget = userData.budget || 0;
        res.status(200).json({ budget });
      } else {
        res.status(404).json({ message: 'User not found' });
      }
    })
    .catch((error) => {
      res.status(500).json({ message: 'Error retrieving budget' });
    });
});

// Rute untuk memperbarui budget
app.put('/budget/:userId', (req, res) => {
  const userId = req.params.userId;
  const { budgetAmount } = req.body;

  // Mengambil referensi ke dokumen pengguna dalam Firestore
  const userDoc = admin.firestore().collection('users').doc(userId);

  // Memperbarui data budget pengguna
  userDoc
    .update({ budget: budgetAmount })
    .then(() => {
      res.status(200).json({ message: 'Budget updated successfully' });
    })
    .catch((error) => {
      res.status(500).json({ message: 'Error updating budget' });
    });
});

// Rute untuk menghapus budget
app.delete('/budget/:userId', (req, res) => {
  const userId = req.params.userId;

  // Mengambil referensi ke dokumen pengguna dalam Firestore
  const userDoc = admin.firestore().collection('users').doc(userId);

  // Menghapus data budget pengguna
  userDoc
    .update({ budget: admin.firestore.FieldValue.delete() })
    .then(() => {
      res.status(200).json({ message: 'Budget deleted successfully' });
    })
    .catch((error) => {
      res.status(500).json({ message: 'Error deleting budget' });
    });
});


// Menjalankan server pada port tertentu
const port = 8080;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
