export interface EnvironmentData {
  environment: string;
  revalidation_interval: number;
}

export type PersistentCategoryData = Pick<CategoryData, "identifier" | "properties" | "destinations">;
export type DynamicCategoryData = Pick<CategoryData, "identifier" | "currentData" | "formatted" | "destinations"> &
  Partial<Pick<CategoryData, "properties">>;

export interface Destination {
  status: string;
  callsign: string;
  format: string;
  ip: string;
  port: number;
}

export interface CategoryData {
  identifier: string;
  properties: {
    ucs: string;
    alias: string;
    updated: string;
  };
  currentData?: {
    database: string;
    size: string;
    data: string;
  };
  formatted?: {
    rt: string;
    rt_plus: string;
    psd: string;
  };
  destinations: Destination[];
}

export interface RDSNetworkData {
  environment: EnvironmentData;
  categories: CategoryData[];
}
