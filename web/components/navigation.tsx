import Link from "next/link";

export interface NavigationLinkProps {
  label: string;
  href: string;
  sub?: string;
  root?: boolean;
  isActive?: boolean;
  Icon: React.ElementType;
}

export const NavigationLink: React.FC<NavigationLinkProps> = ({ label, isActive, Icon, href, sub }) => {
  const fullHref = href + (sub ? sub : "");
  return (
    <Link href={fullHref} className="flex items-center">
      <div className="flex items-center">
        <Icon className={`mr-2 w-5 h-5 ${isActive ? "text-signature" : "text-muted-foreground"}`} />
        <span
          className={`cursor-pointer text-base font-medium ${isActive ? "text-signature" : "text-muted-foreground"}`}
        >
          {label}
        </span>
      </div>
    </Link>
  );
};

export interface NavigationItemProps {
  data: string | number;
  Icon: React.ElementType;
}

export const NavigationItem: React.FC<NavigationItemProps> = ({ data, Icon }) => {
  return (
    <div className="flex items-center">
      <Icon className="mr-2 w-4 h-4 text-muted-foreground" />
      <span className="text-base font-medium text-white">{data}</span>
    </div>
  );
};
