"use client";

import { useState } from "react";
import FiliereSelector from "./FiliereSelector";
import ScoreChart from "./ScoreChart";
import { OrientationRecord } from "../../services/api";

export default function Dashboard() {
  const [selected, setSelected] = useState<OrientationRecord | null>(null);
  const [studentScore, setStudentScore] = useState<string>("");

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-indigo-700">EduStat-TN</h1>
          <p className="mt-1 text-gray-500 text-sm">
            Plateforme BI d'orientation universitaire en Tunisie
          </p>
        </div>

        {/* Filière search */}
        <FiliereSelector onSelect={(r) => setSelected(r)} />

        {/* Student score input */}
        {selected && (
          <div className="rounded-2xl bg-white p-6 shadow-md">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Votre score au Bac (optionnel — pour comparer au seuil)
            </label>
            <input
              type="number"
              step="0.0001"
              min="0"
              max="250"
              placeholder="ex: 105.78"
              value={studentScore}
              onChange={(e) => setStudentScore(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
        )}

        {/* Score chart */}
        {selected && (
          <ScoreChart
            filiereName={`${selected.filiere} — ${selected.etablissement} (${selected.section_bac_nom})`}
            score_2022={selected.score_2022}
            score_2023={selected.score_2023}
            score_2024={selected.score_2024}
            score_2025={selected.score_2025}
            studentScore={studentScore ? parseFloat(studentScore) : null}
          />
        )}

        {!selected && (
          <div className="text-center text-sm text-gray-400 pt-4">
            Recherchez une filière ci-dessus pour voir l'évolution des scores.
          </div>
        )}
      </div>
    </div>
  );
}
