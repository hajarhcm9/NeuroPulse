"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { familyContacts } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";

export default function SOSPage() {
  const router = useRouter();
  const [activated, setActivated] = useState(false);
  const [countdown, setCountdown] = useState(3);
  const [calling, setCalling] = useState(false);
  const [calledContacts, setCalledContacts] = useState<string[]>([]);
  const [showContacts, setShowContacts] = useState(false);
  const [newName, setNewName] = useState("");
  const [newPhone, setNewPhone] = useState("");
  const [contacts, setContacts] = useState(familyContacts);
  const [audioPlaying, setAudioPlaying] = useState(false);

  // Load contacts from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("smart_guardian_contacts");
      if (saved) setContacts(JSON.parse(saved));
    }
  }, []);

  // Save contacts to localStorage
  const saveContacts = (c: typeof contacts) => {
    setContacts(c);
    if (typeof window !== "undefined") {
      localStorage.setItem("smart_guardian_contacts", JSON.stringify(c));
    }
  };

  // SOS countdown
  useEffect(() => {
    if (activated && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
    if (activated && countdown === 0 && !calling) {
      triggerEmergency();
    }
  }, [activated, countdown, calling]);

  // Text-to-speech alert
  const speakAlert = useCallback(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(
        "Alerte! Veuillez vous asseoir dans la chaise la plus proche ou fauteuil et prenez vos medicaments immediatement. Restez calme, de laide est en route."
      );
      utterance.lang = "fr-FR";
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      window.speechSynthesis.speak(utterance);
      setAudioPlaying(true);
      utterance.onend = () => setAudioPlaying(false);
    }
  }, []);

  const triggerEmergency = () => {
    setCalling(true);
    speakAlert();
    // Simulate calling each contact
    contacts.forEach((contact, i) => {
      setTimeout(() => {
        setCalledContacts(prev => [...prev, contact.id]);
      }, (i + 1) * 2000);
    });
  };

  const handleSOS = () => {
    if (!activated) {
      setActivated(true);
      setCountdown(3);
    }
  };

  const cancelSOS = () => {
    setActivated(false);
    setCountdown(3);
    setCalling(false);
    setCalledContacts([]);
    setAudioPlaying(false);
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  };

  const addContact = () => {
    if (newName && newPhone) {
      const newContact = {
        id: String(Date.now()),
        name: newName,
        phone: newPhone,
        relation: "Famille"
      };
      saveContacts([...contacts, newContact]);
      setNewName("");
      setNewPhone("");
    }
  };

  const removeContact = (id: string) => {
    saveContacts(contacts.filter(c => c.id !== id));
  };

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <button onClick={() => router.back()} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Urgence</h1>
      </div>

      {/* SOS Button */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: 30 }}>
        <button
          onClick={handleSOS}
          disabled={activated}
          className={activated ? "" : "sos-pulse"}
          style={{
            width: 180,
            height: 180,
            borderRadius: "50%",
            border: "none",
            background: activated
              ? (calling ? "linear-gradient(135deg, #FF3B30, #FF6B6B)" : "linear-gradient(135deg, #FF9500, #FFCC00)")
              : "linear-gradient(135deg, #FF3B30, #CC0000)",
            color: "white",
            fontSize: activated ? (countdown > 0 ? countdown.toString() : "SOS") : "SOS",
            fontWeight: 900,
            cursor: activated ? "default" : "pointer",
            boxShadow: activated
              ? "0 0 40px rgba(255,59,48,0.6)"
              : "0 0 60px rgba(255,59,48,0.4)",
            transition: "all 0.3s ease",
            position: "relative",
            zIndex: 1,
          }}
        >
          {activated ? (countdown > 0 ? countdown : "SOS") : "SOS"}
        </button>

        {activated && countdown > 0 && (
          <button
            onClick={cancelSOS}
            style={{
              marginTop: 16,
              padding: "10px 28px",
              borderRadius: 14,
              border: "1px solid rgba(255,255,255,0.2)",
              background: "rgba(255,255,255,0.08)",
              color: "white",
              fontSize: 14,
              fontWeight: 600,
              cursor: "pointer"
            }}
          >
            Annuler ({countdown}s)
          </button>
        )}

        {calling && (
          <p style={{ marginTop: 12, fontSize: 13, color: "rgba(255,255,255,0.5)" }}>
            Alerte envoyee - Appels en cours...
          </p>
        )}
      </div>

      {/* Audio Alert Indicator */}
      {audioPlaying && (
        <div style={{
          padding: "14px 18px",
          borderRadius: 16,
          background: "rgba(255,149,0,0.12)",
          border: "1px solid rgba(255,149,0,0.3)",
          marginBottom: 16,
          display: "flex",
          alignItems: "center",
          gap: 12
        }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF9500" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: "#FF9500" }}>Alerte vocale active</div>
            <div style={{ fontSize: 12, color: "rgba(255,255,255,0.5)" }}>Asseyez-vous et prenez vos medicaments</div>
          </div>
        </div>
      )}

      {/* Emergency Buttons */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <button
          onClick={() => {}}
          style={{
            flex: 1,
            padding: "14px",
            borderRadius: 16,
            border: "1px solid rgba(255,59,48,0.3)",
            background: "rgba(255,59,48,0.1)",
            color: "#FF6B6B",
            fontSize: 14,
            fontWeight: 700,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 8
          }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          SAMU (15)
        </button>
        <button
          onClick={() => router.push("/gps")}
          style={{
            flex: 1,
            padding: "14px",
            borderRadius: 16,
            border: "1px solid rgba(123,97,255,0.3)",
            background: "rgba(123,97,255,0.1)",
            color: "#9D8FFF",
            fontSize: 14,
            fontWeight: 700,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 8
          }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
          Ma position
        </button>
      </div>

      {/* Family Contacts - Auto Call Status */}
      <div className="dark-card" style={{ marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: "white" }}>Contacts famille</h2>
          <button
            onClick={() => setShowContacts(!showContacts)}
            style={{ background: "none", border: "none", color: "#7B61FF", fontSize: 13, fontWeight: 600, cursor: "pointer" }}
          >
            {showContacts ? "Fermer" : "Gerer"}
          </button>
        </div>
        <div style={{ fontSize: 12, color: "rgba(255,255,255,0.4)", marginBottom: 12 }}>
          Appel automatique en cas durgence
        </div>
        {contacts.map((contact) => (
          <div
            key={contact.id}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 0",
              borderBottom: "1px solid rgba(255,255,255,0.06)"
            }}
          >
            <div style={{
              width: 40, height: 40, borderRadius: 12,
              background: "rgba(123,97,255,0.15)",
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "#7B61FF", fontWeight: 700, fontSize: 16
            }}>
              {contact.name.charAt(0)}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: "white" }}>{contact.name}</div>
              <div style={{ fontSize: 12, color: "rgba(255,255,255,0.4)" }}>{contact.phone}</div>
            </div>
            {calling && (
              <div style={{
                padding: "4px 10px",
                borderRadius: 10,
                background: calledContacts.includes(contact.id) ? "rgba(52,199,89,0.15)" : "rgba(255,149,0,0.15)",
                fontSize: 11,
                fontWeight: 700,
                color: calledContacts.includes(contact.id) ? "#34C759" : "#FF9500",
                display: "flex",
                alignItems: "center",
                gap: 4
              }}>
                {calledContacts.includes(contact.id) ? (
                  <>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"><path d="M20 6 9 17l-5-5"/></svg>
                    Appele
                  </>
                ) : (
                  <>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" strokeOpacity="0.3"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>
                    Appel...
                  </>
                )}
              </div>
            )}
            {showContacts && !calling && (
              <button
                onClick={() => removeContact(contact.id)}
                style={{ background: "none", border: "none", color: "#FF3B30", cursor: "pointer", fontSize: 12 }}
              >
                Supprimer
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Add Contact Form */}
      {showContacts && !calling && (
        <div className="dark-card" style={{ marginBottom: 16 }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: "white", marginBottom: 12 }}>Ajouter un contact</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="Nom du contact"
              className="input-dark"
            />
            <input
              type="tel"
              value={newPhone}
              onChange={(e) => setNewPhone(e.target.value)}
              placeholder="Numero de telephone"
              className="input-dark"
            />
            <button
              onClick={addContact}
              className="btn-primary"
              style={{ fontSize: 14 }}
            >
              Ajouter
            </button>
          </div>
        </div>
      )}

      <BottomNav />
    </div>
  );
}
