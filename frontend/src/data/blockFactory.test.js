import { describe, it, expect } from 'vitest'
import {
  createEmptyDocument,
  insertBlock,
  deleteBlockDeep,
  findParentId,
  groupWithNext,
  migrateLegacyLayout,
} from './blockFactory'

const TEXT = { block_type: 'Text', block_name: 'Text', default_props: { text: 'hi' } }
const SECTION = { block_type: 'Section', block_name: 'Section', default_props: {} }

describe('blockFactory', () => {
  it('inserts blocks at the requested position', () => {
    const doc = createEmptyDocument()
    const a = insertBlock(doc, 'root', TEXT)
    const b = insertBlock(doc, 'root', TEXT)
    const middle = insertBlock(doc, 'root', TEXT, 1)
    expect(doc.root.data.childrenIds).toEqual([a, middle, b])
  })

  it('gives containers a childrenIds array and non-containers none', () => {
    const doc = createEmptyDocument()
    const section = insertBlock(doc, 'root', SECTION)
    const text = insertBlock(doc, 'root', TEXT)
    expect(doc[section].data.childrenIds).toEqual([])
    expect(doc[text].data.childrenIds).toBeUndefined()
  })

  it('deletes a container together with its descendants', () => {
    const doc = createEmptyDocument()
    const section = insertBlock(doc, 'root', SECTION)
    const child = insertBlock(doc, section, TEXT)
    deleteBlockDeep(doc, section)
    expect(doc[section]).toBeUndefined()
    expect(doc[child]).toBeUndefined()
  })

  it('finds the parent of a nested block', () => {
    const doc = createEmptyDocument()
    const section = insertBlock(doc, 'root', SECTION)
    const child = insertBlock(doc, section, TEXT)
    expect(findParentId(doc, child)).toBe(section)
    expect(findParentId(doc, section)).toBe('root')
    expect(findParentId(doc, 'missing')).toBeNull()
  })

  it('groups a block with its next sibling into one Columns block', () => {
    const doc = createEmptyDocument()
    const a = insertBlock(doc, 'root', TEXT)
    const b = insertBlock(doc, 'root', TEXT)
    const columns = groupWithNext(doc, a)
    expect(doc.root.data.childrenIds).toEqual([columns])
    expect(doc[columns].data.childrenIds).toEqual([a, b])
  })

  it('refuses to group the last block', () => {
    const doc = createEmptyDocument()
    const only = insertBlock(doc, 'root', TEXT)
    expect(groupWithNext(doc, only)).toBeNull()
  })

  it('migrates the legacy nested layout into the flat document', () => {
    const doc = migrateLegacyLayout({
      blocks: [
        {
          id: 'sec',
          block_type: 'Section',
          props: {},
          children: [{ id: 'txt', block_type: 'Text', props: { text: 'hello' } }],
        },
      ],
    })
    expect(doc.root.data.childrenIds).toEqual(['sec'])
    expect(doc.sec.data.childrenIds).toEqual(['txt'])
    expect(doc.txt.data.props.text).toBe('hello')
    expect(doc.root.data.backdropColor).toBeTruthy() // defaults backfilled
  })

  it('survives null / empty / already-migrated layouts', () => {
    expect(migrateLegacyLayout(null).root.data.childrenIds).toEqual([])
    expect(migrateLegacyLayout({}).root.data.childrenIds).toEqual([])
    const current = createEmptyDocument()
    expect(migrateLegacyLayout(current)).toBe(current)
  })
})
