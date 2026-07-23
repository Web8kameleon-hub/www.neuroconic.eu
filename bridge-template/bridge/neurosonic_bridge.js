/**
 * NEUROSONIC BRIDGE - Lidhje me Neurosonic Core (JavaScript/Node.js)
 * Per cdo repo JavaScript/Node.js ne ekosistem.
 * 
 * Perdoret nga: starbooking, web8, etj.
 */

class NeurosonicBridge {
    constructor(repoName, repoUrl = '', port = 9001) {
        this.repoName = repoName;
        this.repoUrl = repoUrl || `https://github.com/Web8kameleon-hub/${repoName}`;
        this.coreUrl = 'http://localhost:8765';
        this.port = port;
        this.status = 'initialized';
        this.lastPulse = null;
        this.bridgeId = this._hash(`${repoName}${Date.now()}`).substring(0, 16);
    }

    _hash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    connect() {
        return { bridge_id: this.bridgeId, repo: this.repoName, status: 'connected' };
    }

    sendPulse(status = 'active') {
        this.lastPulse = {
            bridge_id: this.bridgeId,
            repo: this.repoName,
            status: status,
            timestamp: Date.now() / 1000,
            datetime: new Date().toISOString(),
            hash: this._hash(`${this.repoName}${Date.now()}${status}`)
        };
        return this.lastPulse;
    }

    getStatus() {
        return {
            bridge_id: this.bridgeId,
            repo: this.repoName,
            status: this.status,
            last_pulse: this.lastPulse
        };
    }
}

module.exports = { NeurosonicBridge };
