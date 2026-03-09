const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export interface OrientationRecord {
  id: number;
  code_filiere: string;
  universite: string;
  etablissement: string;
  filiere: string;
  section_bac: string;
  section_bac_nom: string;
  score_2022: number | null;
  score_2023: number | null;
  score_2024: number | null;
  score_2025: number | null;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

type FilterParams = {
  section_bac_nom?: string;
  section_bac?: string;
  universite?: string;
  filiere?: string;
  search?: string;
  page?: number;
};

/**
 * Fetch a paginated list of orientation records.
 * Filter by section_bac_nom, universite, filiere, or free-text search.
 */
export async function fetchOrientations(
  params: FilterParams = {}
): Promise<PaginatedResponse<OrientationRecord>> {
  const query = new URLSearchParams();
  if (params.section_bac_nom)
    query.set("section_bac_nom", params.section_bac_nom);
  if (params.section_bac) query.set("section_bac", params.section_bac);
  if (params.universite) query.set("universite", params.universite);
  if (params.filiere) query.set("filiere", params.filiere);
  if (params.search) query.set("search", params.search);
  if (params.page) query.set("page", String(params.page));

  const res = await fetch(`${BASE_URL}/orientations/?${query.toString()}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

/**
 * Fetch all records for a specific filière (by code_filiere) regardless of page.
 */
export async function fetchFiliereRecords(
  codeFil: string
): Promise<OrientationRecord[]> {
  const res = await fetch(
    `${BASE_URL}/orientations/?code_filiere=${codeFil}&page_size=100`
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  const data: PaginatedResponse<OrientationRecord> = await res.json();
  return data.results;
}
