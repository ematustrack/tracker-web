export interface DataTable {
  foto: string;
  obra: string;
  st: string;
  folio: string;
  profesional: string;
  date: Date;
  lat: number;
  lng: number;
  note: string;
}

export interface DataInTable {
  items: DataTable[];
}
