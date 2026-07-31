// Schema-driven field definitions for the block Inspector, modeled after
// EmailBuilder.js's per-block "Inspect" panel (segmented controls, sliders
// with icon+value, color swatches) rather than generic key/value inputs.

const PADDING_FIELDS = [
  { key: 'paddingTop', label: 'Padding top', control: 'slider', min: 0, max: 80, unit: 'px' },
  {
    key: 'paddingBottom',
    label: 'Padding bottom',
    control: 'slider',
    min: 0,
    max: 80,
    unit: 'px',
  },
  { key: 'paddingLeft', label: 'Padding left', control: 'slider', min: 0, max: 80, unit: 'px' },
  {
    key: 'paddingRight',
    label: 'Padding right',
    control: 'slider',
    min: 0,
    max: 80,
    unit: 'px',
  },
]

const ALIGN_FIELD = {
  key: 'align',
  label: 'Alignment',
  control: 'segmented',
  options: [
    { value: 'left', label: 'Left' },
    { value: 'center', label: 'Center' },
    { value: 'right', label: 'Right' },
  ],
}

export const BLOCK_SCHEMAS = {
  Text: {
    label: 'Text block',
    fields: [
      { key: 'text', label: 'Content', control: 'textarea' },
      { key: 'color', label: 'Text color', control: 'color' },
      { key: 'backgroundColor', label: 'Background color', control: 'color' },
      {
        key: 'fontSize',
        label: 'Font size',
        control: 'slider',
        min: 8,
        max: 96,
        unit: 'px',
      },
      {
        key: 'fontWeight',
        label: 'Font weight',
        control: 'segmented',
        options: [
          { value: 'normal', label: 'Regular' },
          { value: 'bold', label: 'Bold' },
        ],
      },
      ALIGN_FIELD,
      ...PADDING_FIELDS,
    ],
  },
  Button: {
    label: 'Button block',
    fields: [
      { key: 'label', label: 'Text', control: 'text' },
      { key: 'url', label: 'Url', control: 'text' },
      {
        key: 'width',
        label: 'Width',
        control: 'segmented',
        options: [
          { value: 'auto', label: 'Auto' },
          { value: 'full', label: 'Full' },
        ],
      },
      {
        key: 'style',
        label: 'Style',
        control: 'segmented',
        options: [
          { value: 'rectangle', label: 'Rectangle' },
          { value: 'rounded', label: 'Rounded' },
          { value: 'pill', label: 'Pill' },
        ],
      },
      { key: 'textColor', label: 'Text color', control: 'color' },
      { key: 'backgroundColor', label: 'Button color', control: 'color' },
      {
        key: 'fontSize',
        label: 'Font size',
        control: 'slider',
        min: 8,
        max: 48,
        unit: 'px',
      },
      {
        key: 'fontWeight',
        label: 'Font weight',
        control: 'segmented',
        options: [
          { value: 'normal', label: 'Regular' },
          { value: 'bold', label: 'Bold' },
        ],
      },
      ALIGN_FIELD,
      ...PADDING_FIELDS,
    ],
  },
  Image: {
    label: 'Image block',
    fields: [
      { key: 'src', label: 'Image', control: 'image' },
      { key: 'alt', label: 'Alt text', control: 'text' },
      { key: 'width', label: 'Width', control: 'slider', min: 10, max: 100, unit: '%' },
      ALIGN_FIELD,
      ...PADDING_FIELDS,
    ],
  },
  Video: {
    label: 'Video block',
    fields: [
      { key: 'url', label: 'Video URL', control: 'text' },
      { key: 'thumbnail', label: 'Thumbnail URL', control: 'text' },
      ...PADDING_FIELDS,
    ],
  },
  Divider: {
    label: 'Divider block',
    fields: [
      { key: 'color', label: 'Color', control: 'color' },
      {
        key: 'thickness',
        label: 'Thickness',
        control: 'slider',
        min: 1,
        max: 10,
        unit: 'px',
      },
      ...PADDING_FIELDS,
    ],
  },
  Spacer: {
    label: 'Spacer block',
    fields: [
      { key: 'height', label: 'Height', control: 'slider', min: 4, max: 120, unit: 'px' },
      ...PADDING_FIELDS,
    ],
  },
  'Social Icons': {
    label: 'Social icons block',
    fields: [
      { key: 'facebook', label: 'Facebook URL', control: 'text' },
      { key: 'twitter', label: 'Twitter / X URL', control: 'text' },
      { key: 'instagram', label: 'Instagram URL', control: 'text' },
      { key: 'linkedin', label: 'LinkedIn URL', control: 'text' },
      ...PADDING_FIELDS,
    ],
  },
  'Form Field': {
    label: 'Form field block',
    fields: [
      { key: 'label', label: 'Label', control: 'text' },
      { key: 'placeholder', label: 'Placeholder', control: 'text' },
      { key: 'required', label: 'Required', control: 'toggle' },
      {
        key: 'fieldtype',
        label: 'Field type',
        control: 'select',
        options: ['Data', 'Email', 'Phone', 'Textarea'],
      },
      ...PADDING_FIELDS,
    ],
  },
  HTML: {
    label: 'Custom HTML block',
    fields: [
      { key: 'html', label: 'HTML', control: 'textarea', monospace: true },
      ...PADDING_FIELDS,
    ],
  },
  Section: {
    label: 'Section',
    fields: [
      { key: 'backgroundColor', label: 'Background color', control: 'color' },
      ...PADDING_FIELDS,
    ],
  },
  Columns: {
    label: 'Columns',
    fields: [
      { key: 'backgroundColor', label: 'Background color', control: 'color' },
      { key: 'gap', label: 'Gap', control: 'slider', min: 0, max: 40, unit: 'px' },
      ...PADDING_FIELDS,
    ],
  },
  Header: {
    label: 'Header',
    fields: [
      { key: 'backgroundColor', label: 'Background color', control: 'color' },
      ...PADDING_FIELDS,
    ],
  },
  Footer: {
    label: 'Footer',
    fields: [
      { key: 'backgroundColor', label: 'Background color', control: 'color' },
      { key: 'text', label: 'Fallback text', control: 'text' },
      ...PADDING_FIELDS,
    ],
  },
}

// Document-level "Styles" tab (global settings, EmailBuilder.js parity).
export const DOCUMENT_SCHEMA = {
  label: 'Global',
  fields: [
    { key: 'backdropColor', label: 'Backdrop color', control: 'color' },
    { key: 'canvasColor', label: 'Canvas color', control: 'color' },
    { key: 'canvasBorderColor', label: 'Canvas border color', control: 'color' },
    {
      key: 'canvasBorderRadius',
      label: 'Canvas border radius',
      control: 'slider',
      min: 0,
      max: 32,
      unit: 'px',
    },
    {
      key: 'fontFamily',
      label: 'Font family',
      control: 'select',
      options: ['Modern sans', 'Serif', 'Monospace'],
    },
    { key: 'textColor', label: 'Text color', control: 'color' },
  ],
}
