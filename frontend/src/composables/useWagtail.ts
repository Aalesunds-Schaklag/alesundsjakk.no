interface WagtailPage {
  title_no: string
  title_en: string
  content_no: string
  content_en: string
}

export function useWagtail() {
  async function getPage(slug: string): Promise<WagtailPage | null> {
    try {
      const res = await fetch(
        `/api/v2/pages/?slug=${encodeURIComponent(slug)}&type=home.ContentPage&fields=title_en,body_no,body_en`
      )
      if (!res.ok) return null
      const data = await res.json()
      if (!data.items?.length) return null
      const page = data.items[0]
      return {
        title_no: page.title,
        title_en: page.title_en || '',
        content_no: page.body_no || '',
        content_en: page.body_en || '',
      }
    } catch {
      return null
    }
  }

  return { getPage }
}
