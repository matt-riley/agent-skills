local M = {}

M.config = { prefix = "glimpse" }

function M.setup(opts)
  M.config = vim.tbl_deep_extend("force", M.config, opts or {})
  return M.config
end

function M.preview(path)
  return string.format("%s: %s", M.config.prefix, path)
end

return M
