/**
 * NEUROSONIC BRIDGE - Lidhje me Neurosonic Core (TypeScript)
 * Per cdo repo TypeScript ne ekosistem.
 * 
 * Perdoret nga: Cwy, clisonixwesterneurope, ultrawebthinking, etj.
 */

export interface PulseData {
    bridge_id: string;
    repo: string;
    status: string;
    timestamp: number;
    datetime: string;
    hash: string;
    commit?: string;
}

export interface BridgeStatus {
    bridge_id: string;
    repo: string;
    status: string;
    connected: boolean;
    last_pulse: PulseData | null;
    core_url: string;
    port: number;
}

export class NeurosonicBridge {
    public repoName: string;
    public repoUrl: string;
    public coreUrl: string;
    public port: number;
    public status: string;
    public lastPulse: PulseData | null;
    public bridgeId: string;

    constructor(repoName: string, repoUrl: string = '', port: number = 9001) {
        this.repoName = repoName;
        this.repoUrl = repoUrl || `https://github.com/Web8kameleon-hub/${repoName}`;
        this.coreUrl = 'http://localhost:8765';
        this.port = port;
        this.status = 'initialized';
        this.lastPulse = null;
        this.bridgeId = this._simpleHash(`${repoName}${Date.now()}`).substring(0, 16);
    }

    private _simpleHash(str: string): string {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    public connect(): boolean {
        this.status = 'connected';
        return true;
    }

    public sendPulse(status: string = 'active', commit?: string): PulseData {
        const pulse: PulseData = {
            bridge_id: this.bridgeId,
            repo: this.repoName,
            status: status,
            timestamp: Date.now() / 1000,
            datetime: new Date().toISOString(),
            hash: this._simpleHash(`${this.repoName}${Date.now()}${status}`),
            commit: commit
        };
        this.lastPulse = pulse;
        return pulse;
    }

    public getStatus(): BridgeStatus {
        return {
            bridge_id: this.bridgeId,
            repo: this.repoName,
            status: this.status,
            connected: this.status === 'connected',
            last_pulse: this.lastPulse,
            core_url: this.coreUrl,
            port: this.port
        };
    }

    public getStatusBadge(): string {
        const colors: Record<string, string> = {
            connected: 'brightgreen',
            offline: 'red',
            initialized: 'yellow'
        };
        const color = colors[this.status] || 'lightgrey';
        return `![Bridge](https://img.shields.io/badge/Bridge-${this.status}-${color})`;
    }
}

export class Pulse {
    public repoName: string;
    public beats: PulseData[];
    public alive: boolean;

    constructor(repoName: string) {
        this.repoName = repoName;
        this.beats = [];
        this.alive = true;
    }

    public beat(status: string = 'ok'): PulseData {
        const pulse: PulseData = {
            bridge_id: '',
            repo: this.repoName,
            status: status,
            timestamp: Date.now() / 1000,
            datetime: new Date().toISOString(),
            hash: ''
        };
        this.beats.push(pulse);
        return pulse;
    }

    public getStats(): { total_beats: number; alive: boolean; last_beat?: string; seconds_since_last?: number } {
        const total = this.beats.length;
        if (total === 0) return { total_beats: 0, alive: this.alive };
        const last = this.beats[total - 1];
        const secondsSinceLast = Date.now() / 1000 - last.timestamp;
        return {
            total_beats: total,
            alive: secondsSinceLast < 300,
            last_beat: last.datetime,
            seconds_since_last: secondsSinceLast
        };
    }
}

// Example usage
// const bridge = new NeurosonicBridge('Cwy', '', 9005);
// bridge.sendPulse('active');
// console.log(bridge.getStatus());
