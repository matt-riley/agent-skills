local M = {}

function M.render(path, width)
  local text = path or "(no file)"
  if #text > width then
    return text:sub(1, width - 1) .. "…"
  end
  return text
end

return M
