// NEUROSONIC BRIDGE - Lidhje me Neurosonic Core (Go)
// Per cdo repo Go ne ekosistem.
//
// Perdoret nga: OS-CLX

package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"
)

// NeurosonicBridge struct
type NeurosonicBridge struct {
	RepoName  string
	RepoURL   string
	CoreURL   string
	Port      int
	Status    string
	BridgeID  string
	LastPulse *PulseData
}

// PulseData struct
type PulseData struct {
	BridgeID  string `json:"bridge_id"`
	Repo      string `json:"repo"`
	Status    string `json:"status"`
	Timestamp int64  `json:"timestamp"`
	Datetime  string `json:"datetime"`
	Hash      string `json:"hash"`
}

// NewBridge creates a new NeurosonicBridge
func NewBridge(repoName string, repoURL string, port int) *NeurosonicBridge {
	hashInput := fmt.Sprintf("%s%d", repoName, time.Now().UnixNano())
	hash := sha256.Sum256([]byte(hashInput))
	bridgeID := hex.EncodeToString(hash[:])[:16]

	if repoURL == "" {
		repoURL = fmt.Sprintf("https://github.com/Web8kameleon-hub/%s", repoName)
	}

	return &NeurosonicBridge{
		RepoName: repoName,
		RepoURL:  repoURL,
		CoreURL:  "http://localhost:8765",
		Port:     port,
		Status:   "initialized",
		BridgeID: bridgeID,
	}
}

// Connect to Neurosonic Core
func (b *NeurosonicBridge) Connect() bool {
	b.Status = "connected"
	return true
}

// SendPulse sends a pulse signal
func (b *NeurosonicBridge) SendPulse(status string) PulseData {
	hashInput := fmt.Sprintf("%s%d%s", b.RepoName, time.Now().UnixNano(), status)
	hash := sha256.Sum256([]byte(hashInput))

	pulse := PulseData{
		BridgeID:  b.BridgeID,
		Repo:      b.RepoName,
		Status:    status,
		Timestamp: time.Now().Unix(),
		Datetime:  time.Now().UTC().Format(time.RFC3339),
		Hash:      hex.EncodeToString(hash[:])[:16],
	}
	b.LastPulse = &pulse
	return pulse
}

// GetStatus returns bridge status
func (b *NeurosonicBridge) GetStatus() map[string]interface{} {
	connected := b.Status == "connected"
	return map[string]interface{}{
		"bridge_id":  b.BridgeID,
		"repo":       b.RepoName,
		"status":     b.Status,
		"connected":  connected,
		"core_url":   b.CoreURL,
		"port":       b.Port,
		"last_pulse": b.LastPulse,
	}
}

// Pulse system
type Pulse struct {
	RepoName string
	Beats    []PulseData
	Alive    bool
}

// NewPulse creates a new Pulse
func NewPulse(repoName string) *Pulse {
	return &Pulse{
		RepoName: repoName,
		Beats:    []PulseData{},
		Alive:    true,
	}
}

// Beat sends a heartbeat
func (p *Pulse) Beat(status string) PulseData {
	pulse := PulseData{
		Repo:      p.RepoName,
		Status:    status,
		Timestamp: time.Now().Unix(),
		Datetime:  time.Now().UTC().Format(time.RFC3339),
	}
	p.Beats = append(p.Beats, pulse)
	return pulse
}

// GetStats returns pulse statistics
func (p *Pulse) GetStats() map[string]interface{} {
	total := len(p.Beats)
	if total == 0 {
		return map[string]interface{}{
			"total_beats": 0,
			"alive":       p.Alive,
		}
	}
	last := p.Beats[total-1]
	secondsSince := time.Now().Unix() - last.Timestamp
	return map[string]interface{}{
		"total_beats":        total,
		"alive":              secondsSince < 300,
		"last_beat":          last.Datetime,
		"seconds_since_last": secondsSince,
	}
}

func main() {
	bridge := NewBridge("OS-CLX", "", 9004)
	bridge.Connect()
	fmt.Printf("Bridge: %s (%s)\n", bridge.RepoName, bridge.Status)

	pulse := NewPulse("OS-CLX")
	for i := 0; i < 3; i++ {
		p := pulse.Beat("ok")
		fmt.Printf("Pulse #%d: %s\n", i+1, p.Status)
		time.Sleep(100 * time.Millisecond)
	}

	stats := pulse.GetStats()
	fmt.Printf("Stats: %+v\n", stats)
	fmt.Println("Bridge + Pulse: OK")
}
