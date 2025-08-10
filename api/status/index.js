// api/status/index.js (Versi dengan Buku Catatan Ajaib Vercel KV)
import { kv } from '@vercel/kv';

const STATUS_KEY = 'kingdom-status';

async function getInitialStatus() {
    let status = await kv.get(STATUS_KEY);
    if (!status) {
        // Jika buku catatan masih kosong, buat entri baru
        status = {
            last_updated: null,
            components: {
                termux_agent: { status: 'offline', cycles: 0, last_seen: null },
                code_guardian: { status: 'idle', result: 'unknown', last_run: null },
                quantum_pipeline: { status: 'idle', result: 'unknown', last_run: null },
                business_insight: { status: 'idle', result: 'unknown', last_run: null },
                evolution_chamber: { status: 'idle', result: 'unknown', last_run: null },
                self_healing: { status: 'idle', result: 'unknown', last_run: null }
            }
        };
        await kv.set(STATUS_KEY, status);
    }
    return status;
}

export default async function handler(req, res) {
    // Izinkan koneksi dari mana saja (CORS)
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') { return res.status(200).end(); }

    if (req.method === 'POST') {
        try {
            const { component, status, data } = req.body;
            let currentStatus = await getInitialStatus();

            if (component && currentStatus.components[component]) {
                currentStatus.components[component].status = status;
                currentStatus.components[component].last_seen = new Date().toISOString();
                Object.assign(currentStatus.components[component], data);
                currentStatus.last_updated = new Date().toISOString();
                
                await kv.set(STATUS_KEY, currentStatus); // TULIS ke Buku Ajaib!
                
                return res.status(200).json({ message: `Status for ${component} updated.` });
            }
            return res.status(400).json({ error: 'Invalid component.' });
        } catch (e) {
            return res.status(500).json({ error: 'KV write error', details: e.message });
        }
    } 
    
    if (req.method === 'GET') {
        try {
            let currentStatus = await getInitialStatus(); // BACA dari Buku Ajaib!
            
            res.setHeader('Cache-Control', 'no-store'); // Header anti-cache
            return res.status(200).json(currentStatus);
        } catch (e) {
            return res.status(500).json({ error: 'KV read error', details: e.message });
        }
    }
    
    return res.status(405).json({ error: 'Method Not Allowed' });
}
