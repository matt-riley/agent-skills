local M = {}

M.config = { width = 40 }

function M.setup(opts)
  M.config = vim.tbl_deep_extend("force", M.config, opts or {})
  return M.config
end

return M
