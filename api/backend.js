// In Node 18+, fetch is native. We rely on native fetch.
const BASE = process.env.PYTHON_API || 'http://localhost:8000';

async function callPython(path, options = {}) {
    try {
        const res = await fetch(`${BASE}${path}`, options);
        if (!res.ok) {
            const body = await res.text();
            throw new Error(`Python API Error ${res.status}: ${body}`);
        }
        return await res.json();
    } catch (err) {
        if (err.cause && err.cause.code === 'ECONNREFUSED') {
            throw new Error(`Cannot connect to Python backend at ${BASE}. Is uvicorn running on port 8000?`);
        }
        throw err;
    }
}

async function analyzeProfile({ resumeText, jdText, domain }) {
    return await callPython('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText, domain })
    });
}

async function loadDemo(profileKey) {
    return await callPython(`/demo/${profileKey}`);
}

async function getCatalog(domain) {
    const query = domain ? `?domain=${encodeURIComponent(domain)}` : '';
    return await callPython(`/catalog${query}`);
}

async function healthCheck() {
    return await callPython('/health');
}

module.exports = {
    analyzeProfile,
    loadDemo,
    getCatalog,
    healthCheck
};
