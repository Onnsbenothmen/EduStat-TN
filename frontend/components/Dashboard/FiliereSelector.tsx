"use client";

import { useEffect, useState } from "react";
import { fetchOrientations, OrientationRecord } from "../../services/api";

interface Props {
  /** Called when the user picks a filière row */
  onSelect: (record: OrientationRecord) => void;
}

export default function FiliereSelector({ onSelect }: Props) {
  const [search, setSearch] = useState("");
  const [section, setSection] = useState("");
  const [records, setRecords] = useState<OrientationRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!search && !section) {
      setRecords([]);
      return;
    }
    const controller = new AbortController();
    setLoading(true);
    fetchOrientations({ search, section_bac_nom: section || undefined })
      .then((data) => {
        setRecords(data.results);
        setError(null);
      })
      .catch((e) => {
        if (e.name !== "AbortError") setError(e.message);
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [search, section]);

  return (
    <div className="w-full rounded-2xl bg-white p-6 shadow-md">
      <h2 className="mb-4 text-lg font-semibold text-gray-800">
        Rechercher une filière
      </h2>

      <div className="flex gap-3 flex-wrap mb-4">
        <input
          type="text"
          placeholder="Nom filière, établissement…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 min-w-[180px] rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <input
          type="text"
          placeholder="Section Bac (ex: Mathématiques)"
          value={section}
          onChange={(e) => setSection(e.target.value)}
          className="flex-1 min-w-[200px] rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
      </div>

      {loading && (
        <p className="text-sm text-gray-400 animate-pulse">Chargement…</p>
      )}
      {error && <p className="text-sm text-red-500">{error}</p>}

      {records.length > 0 && (
        <div className="overflow-y-auto max-h-64 divide-y divide-gray-100 rounded-lg border border-gray-200">
          {records.map((r) => (
            <button
              key={`${r.code_filiere}-${r.section_bac}`}
              onClick={() => onSelect(r)}
              className="w-full text-left px-4 py-3 hover:bg-indigo-50 transition-colors"
            >
              <span className="block font-medium text-gray-800 text-sm">
                {r.filiere}
              </span>
              <span className="block text-xs text-gray-500">
                {r.etablissement} · {r.section_bac_nom}
              </span>
            </button>
          ))}
        </div>
      )}

      {!loading && records.length === 0 && (search || section) && (
        <p className="text-sm text-gray-400">Aucun résultat trouvé.</p>
      )}
    </div>
  );
}
