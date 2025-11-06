import { useParams } from "react-router";
import BookMatcherPage from "~/components/pages/bookMatcher/BookMatcherPage";

export default function BookMatcher() {
  const { bookId } = useParams<{ bookId: string}>();
  return <BookMatcherPage bookId={bookId}/>
};
