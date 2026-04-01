export interface WagtailPage {
  id: number
  title_no: string
  title_en: string
  content_no: string
  content_en: string
  meta_type: string
  price_items?: PriceItem[]
}

export interface PriceItem {
  category_no: string
  category_en: string
  price_nok: number
  description_no: string
  description_en: string
}

export interface NavItem {
  id: number
  title: string
  title_en: string
  slug: string
  icon: string
  url_path: string
  page_type: string
  vue_route_name: string | null
  children: NavItem[]
}

const ALL_FIELDS = 'title_en,body_no,body_en,icon,show_in_menu,price_items'

function parsePage(page: any): WagtailPage {
  return {
    id: page.id,
    title_no: page.title,
    title_en: page.title_en || '',
    content_no: page.body_no || '',
    content_en: page.body_en || '',
    meta_type: page.meta?.type || '',
    price_items: page.price_items,
  }
}

export function useWagtail() {
  /**
   * Fetch a page by slug. Uses a two-step approach:
   * 1. Find page ID by slug (no model-specific fields needed)
   * 2. Fetch full detail by ID (returns all model-specific fields)
   */
  async function getPage(slug: string): Promise<WagtailPage | null> {
    try {
      // Step 1: find by slug
      const listRes = await fetch(
        `/api/v2/pages/?slug=${encodeURIComponent(slug)}&fields=title`
      )
      if (!listRes.ok) return null
      const listData = await listRes.json()
      if (!listData.items?.length) return null

      // Step 2: fetch detail with all fields
      const pageId = listData.items[0].id
      const detailRes = await fetch(
        `/api/v2/pages/${pageId}/?fields=${ALL_FIELDS}`
      )
      if (!detailRes.ok) return null
      return parsePage(await detailRes.json())
    } catch {
      return null
    }
  }

  /**
   * Fetch a page by its URL path (for nested pages like /om-oss/sjakkhistorie).
   * Extracts the last path segment as slug since slugs are unique across the site.
   */
  async function getPageByPath(path: string): Promise<WagtailPage | null> {
    const segments = path.split('/').filter(Boolean)
    if (!segments.length) return null
    return getPage(segments[segments.length - 1])
  }

  async function getPageChildren(parentId: number): Promise<WagtailPage[]> {
    try {
      const res = await fetch(
        `/api/v2/pages/?child_of=${parentId}&fields=title`
      )
      if (!res.ok) return []
      const data = await res.json()
      // Fetch each child's detail for full fields
      const children: WagtailPage[] = []
      for (const item of data.items || []) {
        const detailRes = await fetch(
          `/api/v2/pages/${item.id}/?fields=${ALL_FIELDS}`
        )
        if (detailRes.ok) {
          children.push(parsePage(await detailRes.json()))
        }
      }
      return children
    } catch {
      return []
    }
  }

  async function getNavigation(): Promise<NavItem[]> {
    try {
      const res = await fetch('/api/v2/navigation/')
      if (!res.ok) return []
      const data = await res.json()
      return data.items || []
    } catch {
      return []
    }
  }

  return { getPage, getPageByPath, getPageChildren, getNavigation }
}
