    /**
    * <p>FastDateParser is a fast and thread-safe version of
    * {@link java.text.SimpleDateFormat}.</p>
    *
    * <p>This class can be used as a direct replacement for
    * <code>SimpleDateFormat</code> in most parsing situations.
    * This class is especially useful in multi-threaded server environments.
    * <code>SimpleDateFormat</code> is not thread-safe in any JDK version,
    * nor will it be as Sun have closed the
    * <a href="http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=4228335">bug</a>/RFE.
    * </p>
    *
    * <p>Only parsing is supported, but all patterns are compatible with
    * SimpleDateFormat.</p>
    *
    * <p>Timing tests indicate this class is as about as fast as SimpleDateFormat
    * in single thread applications and about 25% faster in multi-thread applications.</p>
    *
    * <p>Note that the code only handles Gregorian calendars. The following non-Gregorian
    * calendars use SimpleDateFormat internally, and so will be slower:
    * <ul>
    * <li>ja_JP_TH - Japanese Imperial</li>
    * <li>th_TH (any variant) - Thai Buddhist</li>
    * </ul>
    * </p>
    * @since 3.2
    */
    public class FastDateParser implements DateParser, Serializable {

        // ... (demais membros da classe omitidos) ...

    /**
        * Escape constant fields into regular expression
        * @param regex The destination regex
        * @param value The source field
        * @param unquote If true, replace two success quotes ('') with single quote (')
        * @return The <code>StringBuilder</code>
        */
        private static StringBuilder escapeRegex(StringBuilder regex, String value, boolean unquote) {
            boolean wasWhite= false;
            for(int i= 0; i<value.length(); ++i) {
                char c= value.charAt(i);
                if(Character.isWhitespace(c)) {
                    if(!wasWhite) {
                        wasWhite= true;
                        regex.append("\\s*+");
                    }
                    continue;
                }
                wasWhite= false;
                switch(c) {
                case '\'':
                    if(unquote) {
                        if(++i==value.length()) {
                            return regex;
                        }
                        c= value.charAt(i);
                    }
                    break;
                case '?':
                case '[':
                case ']':
                case '(':
                case ')':
                case '{':
                case '}':
                case '\\':
                case '|':
                case '*':
                case '+':
                case '^':
                case '$':
                case '.':
                    regex.append('\\');
                }
                regex.append(c);
            }
            return regex;
        }

            // ... (demais membros da classe omitidos) ...

    /**
        * A strategy that copies the static or quoted field in the parsing pattern
        */
        private static class CopyQuotedStrategy implements Strategy {
            private final String formatField;

            /**
            * Construct a Strategy that ensures the formatField has literal text
            * @param formatField The literal text to match
            */
            CopyQuotedStrategy(String formatField) {
                this.formatField= formatField;
            }

            /**
            * {@inheritDoc}
            */
            @Override
            public boolean isNumber() {
                char c= formatField.charAt(0);
                if(c=='\'') {
                    c= formatField.charAt(1);
                }
                return Character.isDigit(c);
            }

            /**
            * {@inheritDoc}
            */
            @Override
            public boolean addRegex(FastDateParser parser, StringBuilder regex) {
                escapeRegex(regex, formatField, true);
                return false;
            }

            /**
            * {@inheritDoc}
            */
            @Override
            public void setCalendar(FastDateParser parser, Calendar cal, String value) {
            }
        }
    }