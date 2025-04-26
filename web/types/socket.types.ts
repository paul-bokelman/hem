import type { EnvironmentData, PersistentCategoryData, DynamicCategoryData } from "@/types/data.types";

export type ClientEvent<D, R = void> = (data: D) => Promise<R> | R;

export type ConnectedEvent = ClientEvent<boolean>;
export type EnvironmentDataEvent = ClientEvent<EnvironmentData>;
export type PersistentCategoryDataEvent = ClientEvent<PersistentCategoryData[]>;
export type DynamicCategoryDataEvent = ClientEvent<DynamicCategoryData>;

export interface SocketEvents {
  connected: ConnectedEvent;
  environmentData: EnvironmentDataEvent;
  persistentCategoryData: PersistentCategoryDataEvent;
  dynamicCategoryData: DynamicCategoryDataEvent;
}
