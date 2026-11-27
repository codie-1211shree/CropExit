import { useEffect, useState } from "react";
import {
  getCropCases,
  getCropCase,
  analyzeCrop,
  getRecommendation,
  getScenarios,
  getFinalDecision,
} from "./services/api";

import "./App.css";

function App() {
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);

  const [analysis, setAnalysis] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [scenarios, setScenarios] = useState(null);
  const [decision, setDecision] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load crop cases
  useEffect(() => {
    loadCases();
  }, []);

  const loadCases = async () => {
    try {
      setLoading(true);
      setError("");

      const result = await getCropCases();

      console.log("Crop Cases:", result);

      if (Array.isArray(result)) {
        setCases(result);
      } else if (Array.isArray(result.data)) {
        setCases(result.data);
      } else {
        setCases([]);
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Select a crop case
  const selectCase = async (caseId) => {
    try {
      setLoading(true);
      setError("");

      const result = await getCropCase(caseId);

      const cropCase = result.data || result;

      setSelectedCase(cropCase);

      // Reset old results
      setAnalysis(null);
      setRecommendation(null);
      setScenarios(null);
      setDecision(null);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Run complete AI pipeline
  const runAIAnalysis = async () => {
    if (!selectedCase) return;

    try {
      setLoading(true);
      setError("");

      const caseId = selectedCase.id;

      const analysisResult = await analyzeCrop(caseId);
      setAnalysis(analysisResult);

      const recommendationResult = await getRecommendation(caseId);
      setRecommendation(recommendationResult);

      const scenarioResult = await getScenarios(caseId);
      setScenarios(scenarioResult);

      const decisionResult = await getFinalDecision(caseId);
      setDecision(decisionResult);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>🌱 CropExit AI</h1>
          <p>AI-Powered Crop Loss Prevention & Decision Support</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Backend Connected
        </div>
      </header>

      {/* ERROR */}
      {error && (
        <div className="error">
          ⚠️ {error}
        </div>
      )}

      <main className="container">

        {/* CASE LIST */}
        <section className="card">
          <div className="section-header">
            <div>
              <h2>Crop Cases</h2>
              <p>Select a crop case to analyse</p>
            </div>

            <button onClick={loadCases}>
              Refresh
            </button>
          </div>

          {loading && !selectedCase ? (
            <p>Loading crop cases...</p>
          ) : cases.length === 0 ? (
            <div className="empty">
              No crop cases found.
            </div>
          ) : (
            <div className="case-grid">

              {cases.map((item) => {
                const cropCase = item.data || item;

                return (
                  <div
                    className="case-card"
                    key={cropCase.id}
                    onClick={() => selectCase(cropCase.id)}
                  >
                    <h3>
                      Crop Case
                    </h3>

                    <p>
                      <strong>ID:</strong>{" "}
                      {cropCase.id?.slice(0, 8)}...
                    </p>

                    <p>
                      <strong>Health:</strong>{" "}
                      {cropCase.health_score ?? "N/A"}
                    </p>

                    <p>
                      <strong>Status:</strong>{" "}
                      {cropCase.status ?? "N/A"}
                    </p>

                    <button>
                      View Case
                    </button>
                  </div>
                );
              })}

            </div>
          )}
        </section>


        {/* SELECTED CASE */}
        {selectedCase && (
          <section className="card">

            <h2>🌾 Selected Crop Case</h2>

            <div className="details-grid">

              <div>
                <span>Health Score</span>
                <strong>
                  {selectedCase.health_score ?? "N/A"}
                </strong>
              </div>

              <div>
                <span>Disease Severity</span>
                <strong>
                  {selectedCase.disease_severity ?? "N/A"}
                </strong>
              </div>

              <div>
                <span>Money Invested</span>
                <strong>
                  ₹{selectedCase.money_invested ?? 0}
                </strong>
              </div>

              <div>
                <span>Treatment Cost</span>
                <strong>
                  ₹{selectedCase.treatment_cost ?? 0}
                </strong>
              </div>

              <div>
                <span>Expected Yield</span>
                <strong>
                  {selectedCase.expected_yield ?? "N/A"}
                </strong>
              </div>

              <div>
                <span>Expected Revenue</span>
                <strong>
                  ₹{selectedCase.expected_revenue ?? 0}
                </strong>
              </div>

            </div>

            <button
              className="analyze-btn"
              onClick={runAIAnalysis}
              disabled={loading}
            >
              {loading
                ? "Analysing..."
                : "🤖 Run AI Analysis"}
            </button>

          </section>
        )}

{/* ANALYSIS */}
        {analysis && (
          <section className="card">
            <h2>🤖 AI Analysis</h2>

            <div className="result">
              <div className="score">
                <span>Crop Survival Score</span>
                <strong>
                  {analysis.crop_survival_score ?? "N/A"}
                </strong>
              </div>

              <div>
                <span>Recommendation</span>
                <strong>
                  {typeof analysis.recommendation === "object"
                    ? analysis.recommendation?.recommendation ?? "N/A"
                    : analysis.recommendation ?? "N/A"}
                </strong>
              </div>
            </div>

            {typeof analysis.recommendation === "object" &&
              analysis.recommendation && (
                <div className="recommendation">
                  <p>
                    <strong>Reason: </strong>
                    {analysis.recommendation.reason ?? "N/A"}
                  </p>

                  <p>
                    <strong>Health Score: </strong>
                    {analysis.recommendation.health_score ?? "N/A"}
                  </p>

                  <p>
                    <strong>Disease Severity: </strong>
                    {analysis.recommendation.disease_severity ?? "N/A"}
                  </p>

                  <p>
                    <strong>Recovery Probability: </strong>
                    {analysis.recommendation.recovery_probability ?? "N/A"}%
                  </p>

                  <p>
                    <strong>Expected Revenue: </strong>
                    ₹{analysis.recommendation.expected_revenue ?? 0}
                  </p>

                  <p>
                    <strong>Future Cost: </strong>
                    ₹{analysis.recommendation.future_cost ?? 0}
                  </p>

                  <p>
                    <strong>Projected Profit: </strong>
                    ₹{analysis.recommendation.projected_profit ?? 0}
                  </p>
                </div>
              )}
          </section>
        )}

{/* RECOMMENDATION */}
        {recommendation && (
          <section className="card">
            <h2>💡 Recommendation</h2>

            <div className="recommendation">
              <h3>
                {recommendation.data?.recommendation?.recommendation ??
                  recommendation.data?.recommendation ??
                  recommendation.recommendation?.recommendation ??
                  recommendation.recommendation ??
                  "No recommendation"}
              </h3>

              <p>
                {recommendation.data?.recommendation?.reason ??
                  recommendation.data?.reason ??
                  recommendation.recommendation?.reason ??
                  recommendation.reason ??
                  "No reason available."}
              </p>
            </div>
          </section>
        )}

        {/* SCENARIOS */}
        {scenarios && (
          <section className="card">

            <h2>📊 Investment Scenarios</h2>

            <pre className="json-box">
              {JSON.stringify(scenarios, null, 2)}
            </pre>

          </section>
        )}


        {/* FINAL DECISION */}
        {decision && (
          <section className="card final-card">

            <h2>🎯 Final Decision</h2>

            <pre className="json-box">
              {JSON.stringify(decision, null, 2)}
            </pre>

          </section>
        )}

      </main>

      <footer>
        CropExit AI • Intelligent Crop Loss Prevention
      </footer>

    </div>
  );
}

export default App;