import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load and preprocess training data
data = pd.read_csv('attached_assets/kdd_train (1).csv')

def change_label(df):
    df.labels.replace(['apache2','back','land','neptune','mailbomb','pod','processtable','smurf','teardrop','udpstorm','worm'],'Dos',inplace=True)
    df.labels.replace(['ftp_write','guess_passwd','httptunnel','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','xlock','xsnoop'],'R2L',inplace=True)      
    df.labels.replace(['ipsweep','mscan','nmap','portsweep','saint','satan'],'Probe',inplace=True)
    df.labels.replace(['buffer_overflow','loadmodule','perl','ps','rootkit','sqlattack','xterm'],'U2R',inplace=True)

# Apply label changes
change_label(data)

# Convert labels to numeric
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
data['labels'] = label_encoder.fit_transform(data['labels'])

# Select features used in sample.txt format
features = ['protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'count', 
           'srv_count', 'serror_rate', 'srv_serror_rate', 'same_srv_rate', 
           'diff_srv_rate', 'dst_host_srv_count', 'dst_host_same_srv_rate',
           'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
           'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
           'dst_host_srv_serror_rate', 'dst_host_rerror_rate']

X = data[features]
y = data['labels']

# Encode categorical features
for col in ['protocol_type', 'service', 'flag']:
    X[col] = label_encoder.fit_transform(X[col])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'model.sav')
print("Model trained and saved successfully!")
